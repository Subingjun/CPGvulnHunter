from datetime import datetime
import logging
from pathlib import Path
import socket
import subprocess
import time

from CPGvulnHunter.bridges.joernWrapper import JoernWrapper
from CPGvulnHunter.bridges.llmWrapper import LLMWrapper
from CPGvulnHunter.core.config import ConfigManager, JoernConfig, LoggingConfig
from CPGvulnHunter.core.cpg import CPG
from CPGvulnHunter.passes.initPass import InitPass
from CPGvulnHunter.utils.logger_config import LoggerConfigurator
from CPGvulnHunter.core.passRegistry import PassRegistry


class Task:
    "用于表示一次任务，该任务接收指定的源码，然后执行漏洞检测"
    def __init__(self, target_src_path: str,output_path:str,passes:list[str]=None):
        self.log_config :LoggingConfig = ConfigManager.get_logging_config()
        self.joern_config :JoernConfig = ConfigManager.get_joern_config()
        self.taget_src_path = target_src_path
        self.passes = passes if passes is not None else []  # 默认空列表
        self.base_output_path = Path(output_path)  # 基础输出路径
        self.analysis_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_path = self.base_output_path / f"{Path(target_src_path).name}_{self.analysis_timestamp}"        
        self.output_path.mkdir(parents=True, exist_ok=True)
        LoggerConfigurator.setup_custom_file_handler(
            log_file=str(self.output_path / "task.log"),
            level="INFO",
            max_file_size="50MB",
            backup_count=3
        )
        self.logger = LoggerConfigurator.get_class_logger(self.__class__)
        self.max_task_retries = 3  # 最大重试次数
        self.current_retry = 0
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





    def run(self, run_init_pass: bool = True):
        """
        执行任务，运行所有指定的分析pass
        支持自动重试机制处理服务器崩溃
        """

        return self._execute_task(run_init_pass)

        
    
    def _execute_task(self,run_init_pass: bool = True):
        """
        执行实际的任务逻辑
        """
        self.logger.info(f"开始执行任务 - 源码路径: {self.taget_src_path}, 输出路径: {self.output_path}")
        
        # 初始化CPG对象
        self.cpg = CPG(self.taget_src_path, self.llm_wrapper, self.joern_wrapper)
        assert len(self.cpg.functions) > 0, "CPG初始化失败，未找到任何函数"
        if run_init_pass:
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
        优化后的检测逻辑，更精确地识别服务器崩溃
        """
        crash_indicators = [
            "JOERN_SERVER_CRASHED",      # 我们新的崩溃标识
            "命令执行超时",               # 超时错误
            "连续超时",                   # 连续超时
            "服务器崩溃",                 # 直接的崩溃描述
            "服务器可能已崩溃",           # 可能崩溃
            "连接断开",                   # 连接问题
            "无法连接到Joern服务器",     # 连接失败
            "OutOfMemoryError",          # Java内存错误
            "StackOverflowError",        # Java栈溢出
            "Java heap space",           # Java堆内存不足
            "Connection refused",        # 连接被拒绝
            "Connection reset",          # 连接重置
            "超时",                      # 通用超时
            "timeout"                    # 英文超时
        ]
        
        error_lower = error_msg.lower()
        is_crash = any(indicator.lower() in error_lower for indicator in crash_indicators)
        
        if is_crash:
            self.logger.warning(f"检测到服务器崩溃指示器: {error_msg}")
        
        return is_crash



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
            result = None
            if hasattr(pass_instance, 'run'):
                result = pass_instance.run(str(self.output_path))
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
                raise RuntimeError(f"unknow err: {error_msg}") from e


    
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
                
                
