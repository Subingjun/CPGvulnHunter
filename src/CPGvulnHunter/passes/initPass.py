from abc import ABC, abstractmethod
import logging
from typing import List, Dict, Any, Optional
from enum import Enum
from dataclasses import dataclass
from pathlib import Path

from CPGvulnHunter.core.cpg import CPG
from CPGvulnHunter.models.cpg.function import Function
from CPGvulnHunter.passes.basePass import BasePass
from CPGvulnHunter.utils.threadLogger import get_thread_logger


class InitPassResult():
    """
    初始化Pass的结果数据类
    用于存储InitPass的分析结果
    存储的结果应该如下：
    1. pass_name: str - Pass的名称
    2. cpg所有的函数
    3. cpg的外部函数
    4. cpg的内部函数
    5. cpg的操作符函数
    6. 利用llm分析的函数数量
    7. 生成的语义规则数量
    8. 生成的语义规则
    """
    
    def __init__(self, pass_name: str, cpg: CPG) -> None:
        """
        :param pass_name: Pass的名称
        :param cpg: CPG对象
        """
        self.pass_name = pass_name
        self.cpg = cpg
        self.analyzed_functions_count = len(cpg.functions)
        self.all_functions_count = len(cpg.functions)
        self.external_functions = cpg.external_functions
        self.internal_functions = cpg.internal_functions
        self.operator_functions = cpg.operator_functions
        self.all_functions = cpg.functions
        self.external_functions_count = len(cpg.external_functions)
        self.internal_functions_count = len(cpg.internal_functions)
        self.operator_functions_count = len(cpg.operator_functions)
        self.semantic_rules_count = len(cpg.external_semantics.semantic_list) if cpg.external_semantics else 0
        self.semantics = cpg.external_semantics.to_dict() if cpg.external_semantics else {}

    def to_dict(self) -> Dict[str, Any]:
        """将结果转换为字典格式"""
        return {
            "pass_name": self.pass_name,
            "analyzed_functions_count": self.analyzed_functions_count,
            "all_functions_count": self.all_functions_count,
            "external_functions_count": self.external_functions_count,
            "internal_functions_count": self.internal_functions_count,
            "operator_functions_count": self.operator_functions_count,
            "external_functions": [func.to_dict() for func in self.external_functions],
            "internal_functions": [func.to_dict() for func in self.internal_functions],
            "operator_functions": [func.to_dict() for func in self.operator_functions],
            "semantic_rules_count": self.semantic_rules_count,
            "semantic_rules": self.semantics
        }

class InitPass():
    """
    初始化Pass - 负责外部函数语义分析和应用
    """

    def __init__(self, cpg: CPG) -> None:
        """
        :param cpg: CPG对象
        """
        self.logger = get_thread_logger()
        self.cpg = cpg
        self.name = "initpass"  # 修改为小写，符合文件夹命名规范
        # InitPass不需要sources, sinks等，但需要记录语义分析结果
        self.semantic_rules_count = 0
        self.analyzed_functions_count = 0

    def apply_semantics(self):
        """
        Apply semantics to external functions
        """
        if not self.cpg.llm_wrapper:
            self.logger.error("LLM wrapper is not initialized.")
            return
        
        if not self.cpg.external_functions:
            self.logger.warning("No external functions to analyze.")
            return
            
        self.logger.info(f"开始分析 {len(self.cpg.external_functions)} 个外部函数...")
        self.analyzed_functions_count = len(self.cpg.external_functions)
        
        # analyze external functions nad generate semantics via llm
        self.cpg.external_semantics = self.cpg.llm_wrapper.analyze_external_functions(self.cpg.external_functions)
        if not self.cpg.external_semantics:
            self.logger.error("Failed to generate semantics for external functions.")
            return
            
        self.semantic_rules_count = len(self.cpg.external_semantics.semantic_list)
        self.logger.info(f"生成了 {self.semantic_rules_count} 条语义规则")
        
        # apply semantics to joern cpg
        if not self.cpg.joern_wrapper:
            self.logger.error("Joern wrapper is not initialized.")
            return
        self.cpg.joern_wrapper.apply_semantics(self.cpg.external_semantics)
        self.logger.info(f"Generated {len(self.cpg.external_semantics.semantic_list)} semantic rules for external functions.")

    def get_analysis_results(self) -> InitPassResult:
        """获取InitPass的分析结果"""
        # 收集外部函数信息
        analysis_result = InitPassResult(self.name, self.cpg)
        return analysis_result

    def _save_results(self,output_path:str) -> None:
        """保存分析结果到指定路径"""
        analysis_results = self.get_analysis_results().to_dict()
        with open(output_path, 'w', encoding='utf-8') as f:
            import json
            json.dump(analysis_results, f, ensure_ascii=False, indent=4)
        self.logger.info(f"pass {self.name} 分析结果已保存到 {output_path}")


    def run(self,output_path: Optional[Path] = None) -> None:
        """执行InitPass分析"""
        self.logger.info(f"开始执行 {self.name}")
        # 应用外部函数语义分析
        self.apply_semantics()
        self._save_results(output_path)
        # 保存分析结果
        self.logger.info(f"{self.name} 执行完成")
        return None



