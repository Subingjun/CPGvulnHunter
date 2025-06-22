from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import logging
import json
import yaml
import time
from pathlib import Path

from CPGvulnHunter.bridges.joernWrapper import JoernWrapper
from CPGvulnHunter.bridges.llmWrapper import LLMWrapper
from CPGvulnHunter.models.cpg.function import Function
from CPGvulnHunter.models.cpg.semantics import Semantics
from CPGvulnHunter.core.config import UnifiedConfig
from CPGvulnHunter.utils.logger_config import LoggerConfigurator

class CPG:
    """
    代码属性图（Code Property Graph）数据类
    
    纯数据容器，用于存储 CPG 相关的所有信息
    """
    
    # === 核心必需字段 ===
    src_path: str
    
    # === wrapper ===
    llm_wrapper: Optional[LLMWrapper] = None
    joern_wrapper: Optional[JoernWrapper] = None

    # === 数据容器字段 ===
    functions: List[Function] = []
    external_functions: List[Function] = []
    internal_functions: List[Function] = []
    operator_functions: List[Function] = []
    function_fullName_list: List[str] = []
    functions_info :dict[str:list[str]] = {}# 用于存储函数的详细信息，键为函数全名，值为函数对象
    # === 语义分析字段 ===
    external_semantics: Semantics = None
    
    # === 元数据字段 ===
    metadata: Dict[str, Any] = None
    
    cpg_var: str = "cpg"  # 初始化 cpg_var 属性，默认值为 "cpg"
    

    def __init__(self, src_path: str,llm_wrapper: Optional[LLMWrapper] = None, joern_wrapper: Optional[JoernWrapper] = None):
        self.src_path = src_path
        self.logger = logging.getLogger(__name__)
        self.llm_wrapper = llm_wrapper
        self.joern_wrapper = joern_wrapper
        # 设置日志记录器
        self.logger = logging.getLogger(__name__)
        
        # Ensure logger uses the level from config
        self.logger.info(f"开始初始化CPG - 源路径: {self.src_path}")
        
        # 验证源路径
        src_path_obj = Path(self.src_path)
        if not src_path_obj.exists():
            self.logger.error(f"源代码路径不存在: {self.src_path}")
            raise FileNotFoundError(f"源代码路径不存在: {self.src_path}")
            
        # 导入代码到Joern
        self.logger.info("开始导入代码到Joern创建CPG...")
        try:
            import_start_time = time.time()
            self.joern_wrapper.import_code(self.src_path)
            import_duration = time.time() - import_start_time
            self.logger.info(f"代码导入完成，耗时: {import_duration:.2f}秒")
        except Exception as e:
            self.logger.error(f"代码导入失败: {e}")
            raise
        
        self.logger.info("开始获取所有函数...")
        try:
            self._get_all_functions()
            self.logger.info("所有函数获取成功")
        except Exception as e:
            self.logger.error(f"获取函数失败: {e}")
            raise
        self.logger.info("CPG初始化完成")
        self.logger.info(f"CPG实例创建成功 - 源路径: {self.src_path}, 函数总数: {len(self.functions)}")
        self.logger.debug(f"外部函数总数: {len(self.external_functions)}, 内部函数总数: {len(self.internal_functions)}, 操作符函数总数: {len(self.operator_functions)}")
        self.logger.debug(f"函数全名列表: {self.function_fullName_list}... (总计: {len(self.function_fullName_list)})")
        self.logger.debug(f"cpg_var 初始化为: {self.cpg_var}")
    
    
    def _get_all_functions(self) :
        joern_wrapper = self.joern_wrapper
        if not joern_wrapper:
            self.logger.error("Joern 包装器未初始化")
            return
        try:
            # 获取所有函数 fullName
            self.function_fullName_list = joern_wrapper.get_function_full_names(cpg_var=self.cpg_var)
            self.logger.info(f"发现函数全名总数: {len(self.function_fullName_list)}")
            # 获取所有函数对象
            for full_name in self.function_fullName_list:
                if not full_name:
                    self.logger.warning("函数全名为空，跳过")
                    continue
                function = self._get_single_function(full_name)
                if function and function.full_name:
                    if "<global>" in function.full_name:
                        self.operator_functions.append(function)
                    if function.is_external:
                        if function.full_name.startswith("<operator>"):
                            self.operator_functions.append(function)
                        else:
                            self.external_functions.append(function)
                            self.functions.append(function)
                    else:
                        self.internal_functions.append(function)
                        self.functions.append(function)
            self.logger.info(f"总函数数: {len(self.functions)}")
            self.logger.info(f"外部函数数: {len(self.external_functions)}")
            self.logger.info(f"内部函数数: {len(self.internal_functions)}")
            self.logger.info(f"操作符函数数: {len(self.operator_functions)}")
        except Exception as e:
            self.logger.error(f"获取所有函数失败: {e}")
            raise

    def _get_single_function(self,function_full_name: str) -> Optional[Function]:
        joern_wrapper = self.joern_wrapper
        if not joern_wrapper:
            self.logger.error("Joern wrapper is not initialized.")
            return None
        # 获取单个函数对象
        function = joern_wrapper.get_function_by_full_name(function_full_name, cpg_var=self.cpg_var)
        if not function:
            self.logger.error(f"Function {function_full_name} not found.")
            return None
        
        if function.full_name:
            if function.is_external:
                # fill parameter and useage for external functions,for joern cant generate signature for external functions
                if not function.full_name.startswith("<operator>"):
                    parameters = joern_wrapper.get_parameter(function, cpg_var=self.cpg_var)
                    function.set_parameters(parameters)
                    useage = joern_wrapper.find_useage(function)
                    function.set_useage(useage)                
            return function
        else:
            self.logger.warning(f"Function {function_full_name} not found.")
            return None




