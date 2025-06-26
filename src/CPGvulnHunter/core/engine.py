from asyncio import Task
from dataclasses import dataclass, field
import sys
from typing import List, Dict, Any, Optional, Type, Callable
import logging
from pathlib import Path
import json
import time
from datetime import datetime
import importlib

from CPGvulnHunter.core.cpg import CPG
from CPGvulnHunter.core.config import ConfigManager
from CPGvulnHunter.core.passRegistry import PassRegistry
from CPGvulnHunter.models.AnalysisResult import AnalysisResult
from CPGvulnHunter.passes.basePass import BasePass
from CPGvulnHunter.passes.initPass import InitPass
from CPGvulnHunter.passes.cwe78 import CWE78
from CPGvulnHunter.bridges.llmWrapper import LLMWrapper
from CPGvulnHunter.utils.logger_config import LoggerConfigurator
from CPGvulnHunter.core.task import Task

class VulnerabilityEngine:
    """
    CPG漏洞分析引擎
    
    核心职责：
    1. 管理CPG生命周期
    2. 协调分析passes执行
    3. 收集和处理分析结果
    4. 生成漏洞报告
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
        self.log_config = ConfigManager.get_logging_config()
        self.engine_config = ConfigManager.get_engine_config()
        # 使用LoggerConfigurator设置日志
        LoggerConfigurator.setup_logging(self.log_config)
        self.logger = LoggerConfigurator.get_class_logger(self.__class__)
        self.logger.debug(f"配置文件: {config_file}")
        # 创建输出目录
        self.output_dir = Path(self.engine_config.output_dir)  # 默认输出目录为output
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logger.debug(f"输出目录: {self.output_dir.absolute()}")
        self.logger.info("引擎初始化完成")

    def run(self,src_path: str,passes:list[str]) :
        for retry_count in range(self.engine_config.max_retries):
            retry_count += 1
            try:
                task = Task(target_src_path=src_path, output_path=str(self.output_dir), passes=passes)
                task.run()
            except Exception as e:
                self.logger.error(f"运行任务时发生错误: {e},尝试重启任务")
                continue
        raise RuntimeError("任务执行失败：超出最大重试次数")

    def run_easy_pass(self, src_path: str) -> AnalysisResult:
        """
        """
        task = Task(target_src_path=src_path, output_path=str(self.output_dir), passes=['easyPass'])
        result = task.run(False)
        return result

    def batch_run(self, src_paths: List[str], passes: List[str]) -> List[AnalysisResult]:
        """
        批量运行漏洞分析
        
        Args:
            src_paths: 源代码路径列表
            passes: 分析passes列表
            
        Returns:
            AnalysisResult列表
        """
        results = []
        for src_path in src_paths:
            self.logger.info(f"开始分析源代码: {src_path}")
            result = self.run(src_path, passes)
            results.append(result)
            self.logger.info(f"完成分析源代码: {src_path}")
        return results


if __name__ == "__main__":    
    src_path = "/home/nstl/data/CPGvulnHunter/test/test_case/test2"
    config_file = "/home/nstl/data/CPGvulnHunter/config.yml"
    engine = VulnerabilityEngine(config_file=config_file)
    engine.run(src_path=src_path, passes=['cwe78'])
