from datetime import datetime
import logging
from pathlib import Path
import subprocess
import time

from CPGvulnHunter.bridges.joernWrapper import JoernWrapper
from CPGvulnHunter.bridges.llmWrapper import LLMWrapper
from CPGvulnHunter.core.config import ConfigManager
from CPGvulnHunter.core.cpg import CPG
from CPGvulnHunter.passes.initPass import InitPass
from CPGvulnHunter.utils.logger_config import LoggerConfigurator
from CPGvulnHunter.core.passRegistry import PassRegistry


class Task:
    "用于表示一次任务，该任务接收指定的源码，然后执行漏洞检测"
    def __init__(self, target_src_path: str,output_path:str,passes:list[str]=None):
        self.log_config = ConfigManager.get_logging_config()
        self.taget_src_path = target_src_path
        self.passes = passes if passes is not None else []  # 默认空列表
        self.base_output_path = Path(output_path)  # 基础输出路径
        self.logger = logging.getLogger(__name__)
        # 生成时间戳，用于创建唯一的结果文件夹
        self.analysis_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # 创建以时间戳命名的分析结果文件夹
        self.output_path = self.base_output_path / f"analysis_results_{self.analysis_timestamp}"
        # 确保输出目录存在
        self.output_path.mkdir(parents=True, exist_ok=True)
        self.joern_config = ConfigManager.get_joern_config()
        
        # 任务重试配置
        self.max_task_retries = 3  # 最大重试次数
        self.current_retry = 0
        
        # 初始化包装器
        self._init_wrappers()
    
    def _init_wrappers(self):
        """初始化Joern和LLM包装器"""
        try:
            self.joern_wrapper = JoernWrapper()
            self.logger.info("Joern包装器初始化成功")
        except Exception as e:
            self.logger.error(f"Joern包装器初始化失败: {e}")
            raise
            
        try:
            self.llm_wrapper = LLMWrapper()
            self.logger.info("LLM包装器初始化成功")
        except Exception as e:
            self.logger.error(f"LLM包装器初始化失败: {e}")
            raise
        
    def run(self):
        """
        执行任务，运行所有指定的分析pass
        支持自动重试机制处理服务器崩溃
        """
        for retry_count in range(self.max_task_retries + 1):
            try:
                self.current_retry = retry_count
                if retry_count > 0:
                    self.logger.warning(f"任务重试 {retry_count}/{self.max_task_retries}")
                    # 重新初始化包装器
                    self._reinit_after_crash()
                
                return self._execute_task()
                
            except Exception as e:
                error_msg = str(e)
                
                # 检查是否是Joern服务器崩溃
                if "JOERN_SERVER_CRASHED" in error_msg or self._is_server_crash_error(error_msg):
                    self.logger.error(f"检测到Joern服务器崩溃: {error_msg}")
                    
                    if retry_count < self.max_task_retries:
                        self.logger.info(f"准备重试任务 ({retry_count + 1}/{self.max_task_retries})...")
                        time.sleep(5)  # 等待5秒再重试
                        continue
                    else:
                        self.logger.error(f"任务重试次数已达上限 ({self.max_task_retries})，任务失败")
                        raise RuntimeError(f"任务在{self.max_task_retries}次重试后仍然失败: {error_msg}")
                else:
                    # 非服务器崩溃错误，直接抛出
                    self.logger.error(f"任务执行失败（非服务器崩溃）: {error_msg}")
                    raise
        
        # 理论上不会到达这里
        raise RuntimeError("任务执行失败：超出最大重试次数")
    
    def _execute_task(self):
        """
        执行实际的任务逻辑
        """
        self.logger.info(f"开始执行任务 - 源码路径: {self.taget_src_path}, 输出路径: {self.output_path}")
        
        # 初始化CPG对象
        self.cpg = CPG(self.taget_src_path, self.llm_wrapper, self.joern_wrapper)
        assert len(self.cpg.functions) > 0, "CPG初始化失败，未找到任何函数"
        
        # 单独执行initpass
        InitPass(self.cpg).run(self.output_path / f"initpass.json")
        self.logger.info(f"initPass执行完成，外部函数语义分析结果已保存到 {self.output_path}/initpass.json")
        
        # 执行所有指定的Pass
        results = {}
        for pass_name in self.passes:
            result = self._execute_pass(pass_name)
            results[pass_name] = result
        
        self.logger.info(f"任务执行完成，所有Pass均已成功执行")
        return results
    
    def _is_server_crash_error(self, error_msg: str) -> bool:
        """
        判断是否是服务器崩溃相关的错误
        """
        crash_indicators = [
            "JOERN_SERVER_CRASHED",
            "连续超时",
            "服务器崩溃",
            "连接断开",
            "无法连接到Joern服务器",
            "OutOfMemoryError",
            "StackOverflowError",
            "Java heap space"
        ]
        
        error_lower = error_msg.lower()
        return any(indicator.lower() in error_lower for indicator in crash_indicators)
    
    def _reinit_after_crash(self):
        """
        服务器崩溃后重新初始化
        """
        self.logger.info("开始重新初始化系统组件...")
        
        try:
            # 关闭现有连接
            if hasattr(self, 'joern_wrapper') and self.joern_wrapper:
                try:
                    self.joern_wrapper.close()
                except:
                    pass
            
            # 等待一段时间确保资源清理
            time.sleep(3)
            
            # 重新初始化包装器
            self._init_wrappers()
            
            self.logger.info("系统组件重新初始化完成")
            
        except Exception as e:
            self.logger.error(f"重新初始化失败: {e}")
            raise RuntimeError(f"无法在服务器崩溃后重新初始化: {e}")

    def _execute_pass(self, pass_name: str):
        """
        执行单个分析pass
        
        Args:
            pass_name: Pass名称
            
        Returns:
            AnalysisResult: 该pass的执行结果
        """
        self.logger.info(f"执行Pass: {pass_name}")
        start_time = time.time()

        try:
            # 动态加载Pass类
            pass_class = PassRegistry.get_pass_class(pass_name)
            pass_instance = pass_class(self.cpg)

            # 执行pass
            if hasattr(pass_instance, 'run'):
                result = pass_instance.run(self.output_path)
            execution_time = time.time() - start_time
            self.logger.info(f"Pass {pass_name} 执行成功，耗时: {execution_time:.2f}秒")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = f"Pass {pass_name} 执行失败: {str(e)}"
            self.logger.error(error_msg)
            
            # 检查是否是服务器崩溃错误，如果是则向上传播
            if self._is_server_crash_error(str(e)):
                self.logger.error(f"Pass {pass_name} 中检测到服务器崩溃，传播异常以触发任务重试")
                raise RuntimeError(f"JOERN_SERVER_CRASHED: {error_msg}") from e
            else:
                # 其他错误不重试，直接失败
                raise RuntimeError(error_msg) from e
    
    def get_task_status(self) -> dict:
        """
        获取任务状态信息
        """
        return {
            "target_path": self.taget_src_path,
            "output_path": str(self.output_path),
            "passes": self.passes,
            "current_retry": self.current_retry,
            "max_retries": self.max_task_retries,
            "timestamp": self.analysis_timestamp
        }
    
    def cleanup(self):
        """
        清理任务资源
        """
        try:
            if hasattr(self, 'joern_wrapper') and self.joern_wrapper:
                self.joern_wrapper.close()
            self.logger.info("任务资源清理完成")
        except Exception as e:
            self.logger.warning(f"清理任务资源时出错: {e}")
    
    def __enter__(self):
        """上下文管理器支持"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器退出时清理资源"""
        self.cleanup()
                
                
