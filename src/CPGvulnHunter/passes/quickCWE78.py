#比base pass更快的一个方法
from pathlib import Path
from typing import Any, Dict, List, Optional
from CPGvulnHunter.core.cpg import CPG
from CPGvulnHunter.models.cpg.flowPath import DataFlowResult, FlowPath
from CPGvulnHunter.models.cpg.function import Function
from CPGvulnHunter.models.cpg.sink import Sink
from CPGvulnHunter.models.cpg.source import Source
from CPGvulnHunter.models.llm.dataclass import LLMRequest
from CPGvulnHunter.models.llm.dataflowResult import VulnerabilityResult
from CPGvulnHunter.passes.quickPass import QuickPass
from CPGvulnHunter.utils.llmCacher import LLMCacher
from CPGvulnHunter.utils.threadLogger import get_thread_logger


class QuickCWE78(QuickPass):
    """
    原本的basepass需要上传所有的函数给llm来判别是否是source、sink或santizer,但是这样做的坏处就是太慢了。
    这个pass的流程如下：
    1.获取所有的方法（包含内部方法和外部方法），方法的信息在function内新开一个方法，to_llm_info(),它应该包含
    方法的签名，方法调用点用法，以及方法注解（针对调用点的信息）
    2.整理成一个方法的列表，然后把列表分批交给llm去分析，让它标记潜在的sink、source和santizer
    3.根据第一轮整体分析的结果，开展第二阶段的确认工作，将潜在的source、sink和santizer进行确认，并确认sourcesink的参数位置和类型，用于剩下的污点分析
    4.根据确认后的结果，进行污点分析，剩下的流程和之前的bass pass一致。

    关于缓存部分：
    因为一次性传入的是列表，所以应该缓存方法。方法缓存的key目前可以用方法的签名来做，对于c来说方法签名是我自己生成的，只有可变参数的方法或许需要重新判断。
    对于java来说,fullName可以直接代替方法签名。
    """


    def __init__(self, cpg: CPG):
        self.name = "quickcwe78"
        self.cpg:CPG = cpg
        self.target_functions: List[Function] = self.cpg.functions  # 存储分析目标的函数列表
        self.dataFlowResults: list[DataFlowResult] = []
        self.vulnerabilitiesResults: list[VulnerabilityResult] = []  # 存储漏洞分析结果
        self.logger = get_thread_logger()
        self.potential_source_dict = {}
        self.potential_sink_dict = {}
        self.potential_santizer_dict = {}
        self.sources :list[Source] = []
        self.sinks: list[Sink] = []
        self.sanitizers: list[Function] = []  
        self.cacher = LLMCacher.get_instance()  # 获取LLM缓存实例
        self.vulnerabilitiesResults = []


    def build_classify_method_request(self, funcs: list[Function]) -> LLMRequest:
        func_info_list = [func.to_llm_info() for func in funcs]        
        systemPrompt = """
        你是安全专家，专门检测CWE-78（OS命令注入）漏洞。请严格根据以下标准分析函数：
        - SOURCE: 用户可控输入点（如可能HTTP参数、文件读取、数据库查询结果）
        - SINK: 执行系统命令的函数以及可能调用它的函数（如system(), exec(), popen()等）
        - SANITIZER: 对输入进行安全处理（如过滤特殊字符、白名单校验、转义处理）
        """
        user_prompt = f"""
        ### 函数列表:
        {func_info_list}

        ### 任务要求:
        1. 严格按CWE-78标准分析每个函数的角色
        2. 重点检查命令执行函数和参数传递路径
        3. SOURCE/SINK/SANITIZER可同时为true（如：函数既读取输入又执行命令）
        4. 置信度(confidence)基于证据明确性评估（0.1-1.0）
        5. 原因(reason)需包含具体证据（如调用了system()）

        ### 返回JSON格式:
        {{
            "analysis_result": [
                {{
                    "key": "函数唯一标识",
                    "function_full_name": "完整函数名",
                    "source": true/false,
                    "sink": true/false,
                    "sanitizer": true/false,
                    "confidence": 0.95,
                    "reason": "具体分析依据"
                }}
            ]
        }}

        ### 关键注意:
        - 根据给出的方法相关信息，初步筛选可能是source、sink以及santizer的函数
        """
        return LLMRequest(system_content=systemPrompt, prompt=user_prompt)

    def build_source_confirm_request(self, func: Function) -> LLMRequest:
        """构建确认函数角色的请求（CWE-78命令注入专项）"""
        systemPrompt = """## 角色：命令注入漏洞分析专家
    你专门识别CWE-78（OS命令注入）漏洞中的SOURCE角色。请严格遵循：

    ### SOURCE定义（命令注入场景）
    直接引入外部不可信数据的入口点，包括：
    1. 用户输入函数：`scanf/fgets/getchar/gets`
    2. 命令行参数：`argv`
    3. 环境变量：`getenv`
    4. 网络I/O：`recv/read/recvfrom`
    5. 文件操作：`fread/fgetc/fgets`
    6. Web输入：`CGI_GET/HTTP_POST`等Web接口

    ### 输出规则
    1. 必须返回纯JSON对象，禁止任何额外文本
    2. 参数定位优先级：
    - 0 = this/self对象
    - 1+ = 参数位置（从1开始）
    - -1 = 返回值
    3. 置信度：0.1~1.0（1.0为最高确定性）

    ### 关键判断标准
    ✅ 高危SOURCE特征（命令注入相关）：
    - 参数名含`cmd/command/input/argv`
    - 函数名含`get/read/scan/recv`
    - 来自`stdin/network/file`的数据流
    - 动态构建命令字符串的输入源

    🚫 非SOURCE情况：
    - 仅处理内部数据（无外部交互）
    - 输出型参数（如`printf`的格式化字符串）
    - 命令执行函数本身（如`system()`属于SINK）"""

        user_prompt = f"""
    ## 命令注入SOURCE分析任务
    请分析以下函数在命令注入攻击链中的角色：

    ### 函数信息
    {func.generateFunctionInfo()}

    ### 输出格式（严格JSON）
    ```json
    {{
        "key": "{func.get_function_key()}",
        "function_full_name": "{func.full_name}",
        "source": true/false,
        "parameter_index": 整数,  // 取值：-1(返回值),0(this),1+(参数位置)
        "confidence": 浮点数,   // 0.1~1.0
        "reason": "基于CWE-78的分析依据"
    }}"""
        return LLMRequest(system_content=systemPrompt,prompt=user_prompt)


    def build_sink_confirm_request(self, func: Function) -> LLMRequest:
        """构建确认函数角色的请求"""
        systemPrompt = """你是一个专业的代码安全分析专家，专注于识别CWE-78（OS命令注入）漏洞。
    请分析给定的函数，判断其在命令注入攻击链中的角色，并精确定位具体的参数或返回值。

    角色定义：
    SINK: 可能执行OS命令的危险函数或参数
    - 直接命令执行（如system, exec系列函数）
    - 管道操作（如popen）
    - 脚本解释器调用
    
    **重要：必须精确定位sink的具体参数位置**
    - 参数索引：1表示第一个参数，2表示第二个参数，以此类推
    - 返回值：-1表示函数返回值
    - 对象实例：0表示this/self指针（面向对象方法）"""
        user_prompt = f"""
            请分析以下函数：
            {func.generateFunctionInfo()}
            请确认该函数是否是source，并返回一个json对象，包含以下字段：
            {{
                "key": "{func.get_function_key()}",
                "function_full_name": "{func.full_name}",
                "sink": "true/false",
                "parameter_index": -1, # -1表示返回值 ,1表示第一个参数，2表示第二个参数，以此类推
                "confidence": 0.9,
                "reason": "分析原因"
            }}
    **示例分析思路：**
    - `system(char* command)` → SINK, parameter_index: 1 (第一个参数command是执行点)
    - `execl(const char* path, const char* arg0, ...)` → SINK, parameter_index: 1 (第一个参数path是执行的命令路径)

    **特别注意：**
    - 对于variadic函数（如printf, execl），要考虑所有相关参数
    - 对于缓冲区操作函数，要区分输入缓冲区和输出缓冲区
    - 对于包装函数，要分析实际的数据流向
        """
        return LLMRequest(system_content=systemPrompt,prompt=user_prompt)
                
                
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
        






