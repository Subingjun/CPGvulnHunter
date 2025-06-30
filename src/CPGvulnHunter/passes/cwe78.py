from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from enum import Enum
from dataclasses import dataclass
import logging
from pathlib import Path
from CPGvulnHunter.core.cpg import CPG
from CPGvulnHunter.bridges.llmWrapper import LLMWrapper
from CPGvulnHunter.models.cpg.function import Function
from CPGvulnHunter.models.cpg.source import Source
from CPGvulnHunter.models.cpg.sink import Sink
from CPGvulnHunter.models.cpg.flowPath import DataFlowResult, FlowPath
from CPGvulnHunter.models.llm.dataclass import LLMRequest
from CPGvulnHunter.models.llm.dataflowResult import VulnerabilityResult
from CPGvulnHunter.passes.basePass import BasePass
from CPGvulnHunter.utils.threadLogger import get_thread_logger



class CWE78(BasePass):
    """CWE-78 OS命令注入分析Pass"""
    
    def __init__(self, cpg: CPG):
        super().__init__(cpg)
        self.name = "cwe78_command_injection"

    def build_classify_method_request(self, func: Function) -> LLMRequest:
        """获取函数分析的提示"""
        system_content = """你是一个专业的代码安全分析专家，专注于识别CWE-78（OS命令注入）漏洞。
    请分析给定的函数，判断其在命令注入攻击链中的角色，并精确定位具体的参数或返回值。

    角色定义：
    1. SOURCE: 可能引入不受信任数据的函数或参数
    - 用户输入函数（如scanf, fgets, getchar等）
    - 命令行参数（如argv）
    - 环境变量获取（如getenv）
    - 网络数据接收（如recv, read等）
    - 文件读取函数

    2. SINK: 可能执行OS命令的危险函数或参数
    - 直接命令执行（如system, exec系列函数）
    - 管道操作（如popen）
    - 脚本解释器调用

    3. SANITIZER: 可以清理/验证数据以防止命令注入的函数
    - 输入验证函数
    - 命令转义函数（如escapeshellarg）
    - 白名单过滤函数
    - 参数清理函数

    4. NONE: 与命令注入无关的函数

    **重要：必须精确定位source/sink的具体参数位置**
    - 参数索引：1表示第一个参数，2表示第二个参数，以此类推
    - 返回值：-1表示函数返回值
    - 对象实例：0表示this/self指针（面向对象方法）"""

        user_content = f"""请分析以下函数：

    {func.generateFunctionInfo()}

    请返回一个JSON对象，包含以下字段：
    {{
        "analysis_result": {{
            "function_name": "{func.full_name}",
            "roles": [
                {{
                    "role": "SOURCE|SINK|SANITIZER|NONE",
                    "parameter_index": "具体的参数索引（必填！）",
                    "confidence": "置信度（0.0-1.0）",
                    "reason": "判断理由，必须说明为什么这个具体参数是source/sink点",
                    "parameter_description": "参数描述（如'用户输入的命令字符串'、'待执行的系统命令'等）"
                }}
            ]
        }}
    }}

    **关键分析要求：**
    1. **精确定位参数**：不能只说函数是source/sink，必须明确指出哪个参数是source/sink点
    2. **参数索引准确性**：仔细分析函数签名，确保参数索引正确
    3. **多角色识别**：一个函数可能同时是source和sink（如某些参数是输入，某些参数是输出）
    4. **置信度要求**：只返回置信度 >= 0.6 的结果
    5. **详细说明**：在reason中明确说明为什么该参数是source/sink点

    **示例分析思路：**
    - `system(char* command)` → SINK, parameter_index: 1 (第一个参数command是执行点)
    - `fgets(char* str, int size, FILE* stream)` → SOURCE, parameter_index: 1 (第一个参数str接收用户输入)
    - `scanf("%s", buffer)` → SOURCE, parameter_index: 2 (第二个参数buffer接收用户输入)
    - `char* getenv(const char* name)` → SOURCE, parameter_index: -1 (返回值包含环境变量)
    - `execl(const char* path, const char* arg0, ...)` → SINK, parameter_index: 1 (第一个参数path是执行的命令路径)

    **特别注意：**
    - 对于variadic函数（如printf, execl），要考虑所有相关参数
    - 对于缓冲区操作函数，要区分输入缓冲区和输出缓冲区
    - 对于包装函数，要分析实际的数据流向"""

        return LLMRequest(system_content=system_content, prompt=user_content)


    def build_dataflow_analysis_request(self, path: FlowPath) -> LLMRequest:
        """构建数据流分析的提示"""
        system_content = """你是一个专业的代码安全分析专家，专注于识别CWE-78（OS命令注入）漏洞。
    请分析以下代码，判断其是否可能导致命令注入漏洞。

    **核心分析原则：**
    1. 只有当数据流中包含真正的外部不可信输入时，才可能构成安全漏洞
    2. 纯粹操作硬编码常量、字面量的函数调用不应被视为漏洞源
    3. 必须存在攻击者可控制的数据路径才构成真正的威胁

    **漏洞源（Source）识别规则：**
    - ✅ 有效源：接收外部输入的函数（recv, read, scanf, getenv, argv等）
    - ✅ 有效源：读取外部文件/网络数据的函数
    - ❌ 无效源：仅操作硬编码字符串的函数（如 strcat(buf, "固定字符串")）
    - ❌ 无效源：所有参数都是编译时常量的函数调用

    **数据流分析要求：**
    1. **溯源分析**：追踪到数据的最初来源，确认是否为外部输入
    2. **污点传播**：只有被外部输入"污染"的数据才应被跟踪
    3. **上下文感知**：分析函数调用的具体参数，区分硬编码值和动态输入
    4. **攻击可行性**：评估攻击者是否真正能够控制数据流

    **特殊情况处理：**
    - 如果source函数的所有参数都是硬编码常量 → 不构成漏洞
    - 如果数据流路径中没有真正的外部输入点 → 不构成漏洞  
    - 如果所有中间节点都是硬编码操作 → 不构成漏洞
    - 字符串拼接函数需要检查被拼接的内容是否包含用户可控数据

    **置信度评估标准：**
    - 高置信度 (0.8-1.0)：明确的外部输入直达危险函数，无有效防护
    - 中置信度 (0.5-0.7)：存在外部输入但有部分防护措施
    - 低置信度 (0.1-0.4)：数据流存在但攻击难度很高
    - 无漏洞 (0.0)：无真正的外部输入或已有有效防护

    请返回一个JSON对象，包含以下字段：
    {
        "analysis_result": {
            "is_vulnerable": true|false,  # 是否存在漏洞
            "confidence": "置信度（0.0-1.0）",
            "reason": "详细的判断理由，必须说明数据来源分析和攻击可行性",
            "attack_vector": "具体的攻击向量描述（如果存在漏洞）"
        }
    }
    """

        user_content = f"""请分析以下数据流路径：

    源（source）：{path.source.name}
    汇聚点（sink）：{path.sink.name}

    数据流路径：
    {path.get_path_summary()}

    **分析要求：**
    1. 首先确定source是否为真正的外部输入源
    2. 追踪数据流中每个节点的数据来源
    3. 评估攻击者控制数据的可能性
    4. 判断是否存在有效的防护措施
    5. 给出明确的漏洞判断和理由

    **重点关注：**
    - 如果source函数仅处理硬编码数据，请明确指出这不构成安全风险
    - 如果存在字符串操作函数，请分析其操作的数据是否来源于外部输入
    - 提供具体的数据流分析，而不是泛泛的可能性描述
    """

        return LLMRequest(system_content=system_content, prompt=user_content)







