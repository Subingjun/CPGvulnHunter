import json
import atexit
import logging
import threading
from typing import Optional, Dict, Any
from contextlib import contextmanager

from CPGvulnHunter.models.llm.dataclass import LLMRequest
from CPGvulnHunter.utils.threadLogger import get_thread_logger

class LLMCacher:
    """
    A class to cache LLM responses to avoid redundant API calls.
    这里应该提供三种cache:
    1.senmantics chache
    2. function analysis cache
    3. request cache
    考虑到多线程情况，所有的写cache操作都需要加锁
    使用单例模式
    """
    _instance = None
    _lock = threading.Lock()  # 用于线程安全
    
    def __init__(self, cache_file: str = "llm_cache.json"):
        self.cache_file = cache_file
        self.logger = get_thread_logger()
        self.cache_dir = 'llm_cache'
        self._dirty = False  # 标记缓存是否被修改
        self.senmatics_cache_path = f"{self.cache_dir}/semantic_cache.json"
        self.function_analysis_cache_path = f"{self.cache_dir}/function_analysis_cache.json"
        self.request_cache_path = f"{self.cache_dir}/request_cache.json"
        self.senmatics_cache = self._load_cache(self.senmatics_cache_path)
        self.function_analysis_cache = self._load_cache(self.function_analysis_cache_path)
        self.request_cache = self._load_cache(self.request_cache_path)
        # 注册退出时保存缓存
        atexit.register(self._safe_save_cache)


    def add_semantic_cache(self,key,content) -> Dict[str, Any]|None:
        """添加语义缓存"""
        with self._lock:
            self.senmatics_cache[key] = content
            self._dirty = True
    
    def find_semantic_cache(self,key:str) -> Dict[str, Any]|None:
        """获取语义缓存"""
        return self.senmatics_cache.get(key)

    def add_function_analysis_cache(self, key: str, content) -> None:
        """添加函数分析缓存"""
        with self._lock:
            self.function_analysis_cache[key] = content
            self._dirty = True

    def find_function_analysis_cache(self, key: str) -> Optional[Any]:
        """查找函数分析缓存"""
        if not self.function_analysis_cache:
            return None
        return self.function_analysis_cache.get(key)
    
    def add_request_cache(self, request: LLMRequest, response: dict) -> None:
        """添加请求缓存"""
        with self._lock:
            key = self._calculate_cache_key(request)
            self.request_cache[key] = {"request":request,"response":response}
            self._dirty = True

    def find_request_cache(self, request:str) -> Optional[Any]:
        """查找缓存的响应"""
        if not self.request_cache:
            return None
        key = self._calculate_cache_key(request)
        if key not in self.request_cache:
            return None
        return self.request_cache.get(key).get("response") 



    def __enter__(self):
        """进入上下文管理器"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文管理器时保存缓存"""
        self.save_cache()

    def _load_cache(self,path) -> Dict[str, Any]:
        """加载缓存文件"""
        if self.cache_file:
            try:
                with open(path, 'r+', encoding='utf-8') as f:
                    return json.load(f)
            except (FileNotFoundError, ) as e:
                self.logger.debug(f"缓存文件不存在，创建新文件: {self.cache_file}")
                #不存在则创建新文件
                # 确保目录存在
                import os
                os.makedirs(os.path.dirname(path) if os.path.dirname(path) else '.', exist_ok=True)
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump({}, f, indent=4, ensure_ascii=False)
                self.logger.info(f"成功创建缓存文件: {path}")
                return {}
            except json.JSONDecodeError as e:
                self.logger.error(f"缓存文件 {self.cache_file} 格式错误: {e}")
                return {}
        return {}


    def _calculate_cache_key(self, request) -> str:
        """计算请求的唯一缓存键"""
        import hashlib
        if hasattr(request, '__dict__'):
            request_str = str(sorted(request.__dict__.items()))
        else:
            request_str = str(request)
        
        return hashlib.md5(request_str.encode('utf-8')).hexdigest()

    def save_cache(self):
        """保存三种缓存到对应的文件"""
        try:
            import os

            # 确保缓存目录存在
            os.makedirs(self.cache_dir, exist_ok=True)

            # 保存语义缓存
            if self.senmatics_cache and self._dirty:
                try:
                    with open(self.senmatics_cache_path, 'w', encoding='utf-8') as f:
                        json.dump(self.senmatics_cache, f, indent=4, ensure_ascii=False)
                    self.logger.debug(f"语义缓存已保存到 {self.senmatics_cache_path} ({len(self.senmatics_cache)} 条记录)")
                except Exception as e:
                    self.logger.error(f"保存语义缓存失败: {e}")

            # 保存函数分析缓存
            if self.function_analysis_cache and self._dirty:
                try:
                    with open(self.function_analysis_cache_path, 'w', encoding='utf-8') as f:
                        json.dump(self.function_analysis_cache, f, indent=4, ensure_ascii=False)
                    self.logger.debug(f"函数分析缓存已保存到 {self.function_analysis_cache_path} ({len(self.function_analysis_cache)} 条记录)")
                except Exception as e:
                    self.logger.error(f"保存函数分析缓存失败: {e}")

            # 保存请求缓存
            if self.request_cache and self._dirty:
                try:
                    with open(self.request_cache_path, 'w', encoding='utf-8') as f:
                        json.dump(self.request_cache, f, indent=4, ensure_ascii=False)
                    self.logger.debug(f"请求缓存已保存到 {self.request_cache_path} ({len(self.request_cache)} 条记录)")
                except Exception as e:
                    self.logger.error(f"保存请求缓存失败: {e}")

            # 重置 _dirty 标志
            self._dirty = False

        except Exception as e:
            self.logger.error(f"保存缓存失败: {e}")

    def _safe_save_cache(self):
        """安全保存缓存（用于atexit）"""
        try:
            self.save_cache()
        except:
            pass  # 静默处理退出时的错误

    def __del__(self):
        """析构函数"""
        try:
            if self._dirty:  # 只有在缓存被修改时才保存
                self.save_cache()
        except:
            pass

    @classmethod
    def get_instance(cls) -> "LLMCacher":
        """获取单例实例"""
        if not cls._instance:
            with cls._lock:  # 加锁确保线程安全
                if not cls._instance:
                    cls._instance = cls()  # 创建单例实例
        return cls._instance