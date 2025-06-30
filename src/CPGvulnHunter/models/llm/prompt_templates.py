from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Any

class VulnerabilityType(Enum):
    SQL_INJECTION = "SQL Injection (CWE-89)"
    BUFFER_OVERFLOW = "Buffer Overflow (CWE-120)"
    XSS = "Cross-site Scripting (CWE-79)"
    PATH_TRAVERSAL = "Path Traversal (CWE-22)"
    COMMAND_INJECTION = "OS Command Injection (CWE-78)"

@dataclass
class PromptTemplate:
    system_content: str
    user_content: str
    examples: List[Dict[str, Any]]

class PromptTemplateManager:
    
    @staticmethod
    def get_classify_template(vuln_type: VulnerabilityType) -> PromptTemplate:
        """获取函数角色分类提示词模板"""
        templates = {
            VulnerabilityType.SQL_INJECTION: PromptTemplate(
                system_content="""您是一个专业的代码安全分析专家，专注于识别SQL注入漏洞(CWE-89)。
请分析给定的函数，判断其在SQL注入攻击链中的角色，并精确定位具体的参数或返回值。

角色定义：
1. SOURCE: 可能引入不受信任数据的函数或参数
- 用户输入函数(如scanf, gets, fgets等)
- HTTP请求参数获取函数
- 数据库查询结果处理函数
- 文件读取函数

2. SINK: 可能执行SQL查询的危险函数或参数
- 数据库查询函数(如mysql_query, sqlite3_exec)
- ORM查询构建函数
- 预处理语句拼接函数

3. SANITIZER: 可以防止SQL注入的函数
- 参数化查询函数
- 输入转义函数(如mysql_real_escape_string)
- 白名单验证函数

4. NONE: 与SQL注入无关的函数""",
                user_content="""请分析以下函数：
{function_info}

请返回JSON对象，包含：
{{
    "analysis_result": {{
        "function_name": "{function_name}",
        "roles": [
            {{
                "role": "SOURCE|SINK|SANITIZER|NONE",
                "parameter_index": "参数索引(1=第一个参数,-1=返回值)",
                "confidence": "置信度(0.0-1.0)",
                "reason": "判断理由",
                "parameter_description": "参数描述"
            }}
        ]
    }}
}}""",
                examples=[
                    {
                        "function": "void queryUser(char* username)",
                        "analysis": {
                            "role": "SINK",
                            "parameter_index": 1,
                            "reason": "参数username直接拼接到SQL查询中"
                        }
                    }
                ]
            ),
            
            VulnerabilityType.BUFFER_OVERFLOW: PromptTemplate(
                system_content="""您是一个专业的代码安全分析专家，专注于识别缓冲区溢出漏洞(CWE-120)。""",
                # 类似结构其他漏洞模板
                user_content="",
                examples=[]
            ),
            
            VulnerabilityType.XSS: PromptTemplate(
                system_content="""您是一个专业的代码安全分析专家，专注于识别XSS漏洞(CWE-79)。""",
                user_content="",
                examples=[]
            ),
            
            VulnerabilityType.PATH_TRAVERSAL: PromptTemplate(
                system_content="""您是一个专业的代码安全分析专家，专注于识别路径遍历漏洞(CWE-22)。""",
                user_content="",
                examples=[]
            )
        }
        return templates[vuln_type]

    @staticmethod
    def get_dataflow_template(vuln_type: VulnerabilityType) -> PromptTemplate:
        """获取数据流分析提示词模板"""
        templates = {
            VulnerabilityType.SQL_INJECTION: PromptTemplate(
                system_content="""您是一个专业的代码安全分析专家，专注于识别SQL注入漏洞(CWE-89)。
请分析以下数据流路径，判断是否可能导致SQL注入。""",
                user_content="""请分析数据流路径：
源(source): {source_name}
汇聚点(sink): {sink_name}

数据流路径:
{path_summary}

请返回JSON对象，包含：
{{
    "analysis_result": {{
        "is_vulnerable": true|false,
        "confidence": "置信度(0.0-1.0)",
        "reason": "详细分析",
        "attack_vector": "攻击向量描述(如存在)"
    }}
}}""",
                examples=[]
            ),
            # 其他漏洞类型的数据流模板
        }
        return templates[vuln_type]
