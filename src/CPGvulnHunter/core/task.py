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
        """
        self.logger.info(f"开始执行任务 - 源码路径: {self.taget_src_path}, 输出路径: {self.output_path}")
        
        # 初始化CPG对象
        self.cpg = CPG(self.taget_src_path,self.llm_wrapper, self.joern_wrapper)
        assert len(self.cpg.functions) > 0, "CPG初始化失败，未找到任何函数"
        #单独执行initpass
        InitPass(self.cpg).run(self.output_path / f"initpass.json")
        self.logger.info(f"initPass执行完成，外部函数语义分析结果已保存到 {self.output_path}/initpass.json")
        
        # 执行所有指定的Pass
        results = []
        for pass_name in self.passes:
            result = self._execute_pass(pass_name)
            results.append(result)
        
        self.logger.info("所有Pass执行完成")

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
                    pass_instance.run(self.output_path)
                execution_time = time.time() - start_time
                self.logger.info(f"Pass {pass_name} 执行成功，耗时: {execution_time:.2f}秒")
                
            except Exception as e:
                execution_time = time.time() - start_time
                error_msg = f"Pass {pass_name} 执行失败: {str(e)}"
                self.logger.error(error_msg)
                
                

