from asyncio import Task
from concurrent import futures
from dataclasses import dataclass, field
import sys
from typing import List, Dict, Any, Optional, Type, Callable
import logging
from pathlib import Path
import json
import time
from datetime import datetime
import importlib

import concurrent
from concurrent.futures import ThreadPoolExecutor

from CPGvulnHunter.bridges.joernServerPool import JoernServerPool
from CPGvulnHunter.core.cpg import CPG
from CPGvulnHunter.core.config import ConfigManager
from CPGvulnHunter.core.passRegistry import PassRegistry
from CPGvulnHunter.models.AnalysisResult import AnalysisResult
from CPGvulnHunter.passes.basePass import BasePass
from CPGvulnHunter.passes.initPass import InitPass
from CPGvulnHunter.passes.cwe78 import CWE78
from CPGvulnHunter.bridges.llmWrapper import LLMWrapper
from CPGvulnHunter.utils.logger_config import LoggerConfigurator
from CPGvulnHunter.utils.threadLogger import get_thread_logger
from CPGvulnHunter.core.task import Task

class VulnerabilityEngine:
    """
 
    """
    
    def __init__(self, 
                 config_file: Optional[str] = None):
        """
        初始化漏洞分析引擎
        
        Args:
            config_file: 配置文件路径
            config: 统一配置对象（与config_file二选一）
        """        
        # 初始化配置管理器
        ConfigManager.initialize(config_file)
        self.engine_config = ConfigManager.get_engine_config()
        # 使用LoggerConfigurator设置日志
        self.logger = logging.getLogger("CPGVulnHunter")
        self.logger.debug(f"配置文件: {config_file}")
        # 创建输出目录
        self.output_dir = Path(self.engine_config.output_dir)  # 默认输出目录为output
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logger.debug(f"输出目录: {self.output_dir.absolute()}")
        self.logger.info("引擎初始化完成")
        self.max_workers = 0


    def run(self,src_path: list[str],passes:list[str]) :
        # for retry_count in range(self.engine_config.max_retries):
        #     retry_count += 1
        #     try:
        #         task = Task(target_src_path=src_path, output_path=str(self.output_dir), passes=passes)
        #         task.run()
        #     except Exception as e:
        #         self.logger.error(f"运行任务时发生错误: {e},尝试重启任务")
        #         continue
        # raise RuntimeError("任务执行失败：超出最大重试次数")
        self.batch_run_mutipul_thread(src_path,passes,1)

    def batch_run(self, src_paths: List[str], passes: List[str],threads:int) -> List[Dict[str, Any]]:
        self.batch_run_mutipul_thread(src_paths, passes,threads)


    # 由于gil锁，多线程感觉没啥用，效率上面没什么太大提升。
    def batch_run_mutipul_thread(self, src_paths: List[str], passes: List[str],threads:int) -> List[Dict[str, Any]]:
        """
        批量运行漏洞分析 - 多线程版本
        
        Args:
            src_paths: 源代码路径列表
            passes: 分析passes列表
            
        Returns:
            结果字典列表
        """
        self.max_workers = threads
        if not src_paths:
            return []
        #初始化joern服务器池子
        self.joern_server_pool = JoernServerPool.get_instance()
        # 有多少个线程，就开多少个服务器。
        self.joern_server_pool.configure(server_number=threads)
        self.joern_server_pool.start_pool()
        self.logger.info(f"开始批量分析 {len(src_paths)} 个项目，使用 {self.max_workers} 个工作线程")
        
        results = []
        
        # 使用ThreadPoolExecutor执行任务
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 提交所有任务
            future_to_src = {
                executor.submit(self._run_single_task, src_path, passes): src_path
                for src_path in src_paths
            }
            
            # 收集结果
            for future in futures.as_completed(future_to_src):
                src_path = future_to_src[future]
                try:
                    result = future.result()
                    results.append(result)
                    
                    if result['status'] == 'success':
                        self.logger.info(f"任务成功完成: {src_path}")
                    else:
                        self.logger.error(f"任务执行失败: {src_path}", exc_info=True)
                        
                except Exception as exc:
                    self.logger.error(f"任务执行异常: {src_path}, 异常: {exc}", exc_info=True)
                    results.append({
                        'status': 'exception',
                        'src_path': src_path,
                        'error': str(exc)
                    })
        
        # 统计结果
        success_count = sum(1 for r in results if r['status'] == 'success')
        error_count = len(results) - success_count
        
        self.logger.info(f"批量分析完成 - 成功: {success_count}, 失败: {error_count}")
        return results





    def _run_single_task(self, src_path: str, passes: List[str]) -> Dict[str, Any]:
            """
            运行单个任务的线程函数
            
            Args:
                src_path: 源代码路径  
                passes: 分析passes列表
                
            Returns:
                包含结果和状态的字典
            """
            import threading
            import asyncio
            thread_id = threading.current_thread().ident
            
            # 修复：为每个线程初始化事件循环，防止JoernBridge连接报错
            try:
                asyncio.get_running_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            try:
                logger = get_thread_logger()
                # Task会设置线程专用的logger
                task = Task(
                    target_src_path=src_path,
                    output_path=str(self.output_dir),
                    passes=passes,
                )
                
                # 现在可以使用线程logger
                logger.info(f"线程 {thread_id} 开始处理任务: {src_path} ")
                
                # 重试逻辑
                for retry_count in range(self.engine_config.max_retries):
                    try:
                        result = task.run()
                        logger.info(f"线程 {thread_id} 任务完成: {src_path}")
                        return {
                            'status': 'success',
                            'src_path': src_path,
                            'result': result,
                            'thread_id': thread_id,
                        }
                    except Exception as task_error:
                        logger.warning(f"线程 {thread_id} 任务重试 {retry_count + 1}/{self.engine_config.max_retries}: {src_path}, 错误: {task_error}")
                        if retry_count == self.engine_config.max_retries - 1:
                            raise task_error
                        time.sleep(1)  # 重试前等待
                        
            except Exception as e:
                # 如果logger还没初始化，使用打印
                if logger:
                    logger.error(f"线程 {thread_id} 任务失败: {src_path}, 错误: {e}", exc_info=True)
                else:
                    print(f"线程 {thread_id} 任务失败: {src_path}, 错误: {e}")
                    
                return {
                    'status': 'error',
                    'src_path': src_path,
                    'error': str(e),
                    'thread_id': thread_id,
                }



if __name__ == "__main__":    
    src_path = "/home/nstl/data/CPGvulnHunter/test/test_case/test2"
    config_file = "/home/nstl/data/CPGvulnHunter/config.yml"
    engine = VulnerabilityEngine(config_file=config_file)
    engine.run(src_path=src_path, passes=['cwe78'])
