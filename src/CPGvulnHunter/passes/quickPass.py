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
from CPGvulnHunter.utils.llmCacher import LLMCacher
from CPGvulnHunter.utils.threadLogger import get_thread_logger


class QuickPass():
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
        self.name = "quickpass"
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


    def find_potential_target(self):
        """
        分析所有函数，将其分类为source、sink或sanitizer。
        这里使用LLM来分析函数的角色，并将结果存储在self.sources, self.sinks和self.sanitizers中。
        把他们加入到dick里面，后续进行确认。
        """
        function_list :list[Function] = self.target_functions
        #十个一组，传给大模型进行第一阶段分析
        batch_size = 10
        for i in range(0, len(function_list), batch_size):
            batch = function_list[i:i + batch_size]
            request = self.build_classify_method_request(batch)
            response = self.cpg.llm_wrapper.analysisi_function(request)
            if not response or 'analysis_result' not in response:
                self.logger.warning(f"LLM分析结果为空或格式不正确: {response}")
                return
            analysis_result = response.get('analysis_result', [])
            for result in analysis_result:
                function_full_name = result.get('function_full_name')
                if not function_full_name:
                    self.logger.warning("分析结果中缺少函数全名")
                    continue
                function = self.cpg.get_function_by_full_name(function_full_name)
                if not function:
                    self.logger.error(f"未找到大模型传回的函数: {function_full_name}，有可能是大模型拼错了函数全名。")
                    continue
                function_key = function.get_function_key()
                isSource = result.get('source', False) 
                isSink = result.get('sink', False)
                isSanitizer = result.get('sanitizer', False)
                if isinstance(isSource, str):
                    isSource = self.string_to_boolean(isSource)
                if isinstance(isSink, str):
                    isSink = self.string_to_boolean(isSink)
                if isinstance(isSanitizer, str):
                    isSanitizer = self.string_to_boolean(isSanitizer)
                # 加入潜在备选名单
                if isSource:
                    self.potential_source_dict[function_key] = function
                if isSink:
                    self.potential_sink_dict[function_key] = function
                if isSanitizer:
                    self.potential_santizer_dict[function_key] = function
        self.logger.debug(f"潜在的source函数: {self.potential_source_dict}")
        self.logger.debug(f"潜在的sink函数: {self.potential_sink_dict}")
        self.logger.debug(f"潜在的sanitizer函数: {self.potential_santizer_dict}")
        return {'source': self.potential_source_dict,
                'sink': self.potential_sink_dict,
                'sanitizer': self.potential_santizer_dict}

        


    def string_to_boolean(self, value: str) -> bool:
        """将字符串转换为布尔值"""
        if value.lower() in ['true', '1', 'yes']:
            return True
        elif value.lower() in ['false', '0', 'no']:
            return False
        else:
            raise ValueError(f"无法将字符串 '{value}' 转换为布尔值")


    def build_classify_method_request(self, funcs: list[Function]) -> LLMRequest:
        func_info_list = [func.to_llm_info() for func in funcs]        
        systemPrompt = """你是漏洞挖掘专家，请查看如下的函数列表，根据提供的信息分析其中可能存在的漏洞source，sink和sanitizer。"""
        user_prompt = f"""
            列表如下：
            {func_info_list}
            请分析每个函数的角色，并返回一个列表，包含每个函数的角色
            角色可以是source、sink或sanitizer，或者None。
            要求用json返回结构，返回的结果应如下：
            {{
                "analysis_result": [
                    {{                        
                        "key": "function_key",
                        "function_full_name": "function_full_name",
                        "source": "true/false",
                        "sink": "true/false",
                        "sanitizer": "true/false",
                        "confidence": 0.9,
                        "reason": "分析原因"
                    }},
                ]   
            }}
        """
        return LLMRequest(system_content=systemPrompt,prompt=user_prompt)



    def confirm_potential(self) -> None:
        """对潜在的souruce sink进行二次分析，确定是否为souce、sink或sanitizer，并确定相应的参数"""
        for source in self.potential_source_dict.values():
            request = self.build_source_confirm_request(source)
            response = self.cpg.llm_wrapper.analysisi_function(request)
            if not response or 'source' not in response:
                self.logger.warning(f"LLM确认结果为空或格式不正确: {response}")
                continue
            if response.get('source', False):
                index = response.get('parameter_index', -1)
                self.logger.info(f"确认函数 {source.full_name} 为source，参数为 {index}")
                self.sources.append(Source.create_from_function(source,index=index))
        for sink in self.potential_sink_dict.values():
            request = self.build_sink_confirm_request(sink)
            response = self.cpg.llm_wrapper.analysisi_function(request)
            if not response or 'sink' not in response:
                self.logger.warning(f"LLM确认结果为空或格式不正确: {response}")
                continue
            if response.get('sink', False):
                index = response.get('parameter_index')
                self.logger.info(f"确认函数 {sink.full_name} 为sink,参数为{index}")
                self.sinks.append(Sink.create_from_function(sink,index=index))




    def build_source_confirm_request(self, func: Function) -> LLMRequest:
        """构建确认函数角色的请求"""
        systemPrompt = """你是漏洞挖掘专家，请判断函数是否是source"""
        user_prompt = f"""
            函数信息如下：
            {func.generateFunctionInfo()}
            请确认该函数的角色，并返回一个json对象，包含以下字段：
            {{
                "key": "{func.get_function_key()}",
                "function_full_name": "{func.full_name}",
                "source": "true/false",
                "parameter_index": -1, # -1表示返回值 ,1表示第一个参数，2表示第二个参数，以此类推
                "confidence": 0.9,
                "reason": "分析原因"
            }}
    **重要：必须精确定位source/sink的具体参数位置**
    - 参数索引：1表示第一个参数，2表示第二个参数，以此类推
    - 返回值：-1表示函数返回值
    - 对象实例：0表示this/self指针（面向对象方法）
        """
        return LLMRequest(system_content=systemPrompt,prompt=user_prompt)

    def build_sink_confirm_request(self, func: Function) -> LLMRequest:
        """构建确认函数角色的请求"""
        systemPrompt = """你是漏洞挖掘专家，请判断函数是否是sink"""
        user_prompt = f"""
            函数信息如下：
            {func.generateFunctionInfo()}
            请确认该函数的角色，并返回一个json对象，包含以下字段：
            {{
                "key": "{func.get_function_key()}",
                "function_full_name": "{func.full_name}",
                "sink": true/false,
                "parameter_index": -1, # -1表示返回值 ,1表示第一个参数，2表示第二个参数，以此类推
                "confidence": 0.9,
                "reason": "分析原因"
            }}
    **重要：必须精确定位source/sink的具体参数位置**
    - 参数索引：1表示第一个参数，2表示第二个参数，以此类推
    - 返回值：-1表示函数返回值
    - 对象实例：0表示this/self指针（面向对象方法）
        """
        return LLMRequest(system_content=systemPrompt,prompt=user_prompt)







    def taint_analysis(self)  -> None:
        """执行污点分析"""
        if not self.cpg.joern_wrapper:
            self.logger.error("Joern wrapper未初始化，无法执行污点分析")
            return None
        semantics = self.cpg.external_semantics
        if not semantics or len(semantics.semantic_list) == 0:
            self.logger.error("没有可用的语义规则，五点分析可能存在问题！")
        for source in self.sources:
            for sink in self.sinks:
                dataflow_result = self.cpg.joern_wrapper.run_taint_analysis(
                    source,
                    sink
                )
                if not dataflow_result or dataflow_result.flows is None or len(dataflow_result.flows) == 0:
                    self.logger.info(f"源 {source.full_name} 到汇聚点 {sink.full_name} 的数据流分析未找到路径")
                    continue
                self.dataFlowResults.append(dataflow_result)
                self.logger.info(f"分析源 {source.full_name} 到汇聚点 {sink.full_name} 的数据流结果: {dataflow_result}")              
        self.logger.info(f"污点分析完成，共找到 {len(self.dataFlowResults)} 个数据流结果")
        return None

    def vuln_analysis(self):
        self.logger.info("开始执行漏洞数据流链条分析")
        if not self.cpg.joern_wrapper:
            self.logger.error("Joern wrapper未初始化，无法执行数据流分析")
            return None
        for result in self.dataFlowResults:
            self.logger.debug(f"开始分析数据流: {result}")
            for flow in result.flows:
                self.logger.info(f"分析数据流路径: {flow}")
                request = self.build_dataflow_analysis_request(flow)
                self.logger.debug(f"构建的数据流分析请求: {request.prompt}")
                llm_result  = self.cpg.llm_wrapper.analyze_dataflow(request)
                # 将结果转换为 DataflowResult 类型
                if llm_result and 'analysis_result' in llm_result:
                    llm_result = llm_result['analysis_result']
                    analysis_result = VulnerabilityResult(
                        source=result.source.to_dict(),
                        sink=result.sink.to_dict(),
                        is_vulnerable=llm_result.get('is_vulnerable', None),
                        confidence=llm_result.get('confidence', None),
                        reason=llm_result.get('reason', None),
                        flowPath_code=flow._get_function_chain(),
                        flows=flow
                    )
                    self.vulnerabilitiesResults.append(analysis_result)
                    self.logger.info(f"数据流分析结果: {analysis_result}")
                
                
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

    def get_analysis_results(self) -> Dict[str, Any]:
        """获取分析结果，包含当前pass的所有信息"""
        project_info = {
            'name': self.cpg.src_path
        }
        sources_info = [source.to_dict() for source in self.sources]
        sinks_info = [sink.to_dict() for sink in self.sinks]
        sanitizers_info = [sanitizer.to_dict() for sanitizer in self.sanitizers]
        data_flow_results_info = [result.to_dict() for result in self.dataFlowResults]
        vulnerabilities_info = [vuln.to_dict() for vuln in self.vulnerabilitiesResults]
        result_info = {
            'project_info' : project_info,
            'analysis_results': vulnerabilities_info,
            'sources': sources_info,
            'sinks': sinks_info,
            'sanitizers': sanitizers_info,
            'data_flow_results': data_flow_results_info
        }
        self.logger.info(f"获取分析结果: {result_info}")
        return result_info
    
    
    def _save_results(self,output_path:str) -> None:
        """保存分析结果到指定路径"""
        try:
            analysis_results = self.get_analysis_results()
            # 修复路径操作：确保output_dir是Path对象
            output_dir = Path(output_path)
            
            # 生成时间戳文件夹（所有pass共享同一个时间戳文件夹）
            from datetime import datetime
            
            # 每个pass保存为单独的文件
            pass_name = self.name.lower().replace(" ", "_").replace("-", "_")
            save_path = output_dir / f"{pass_name}.json"
            
            with open(save_path, 'w', encoding='utf-8') as f:
                import json
                json.dump(analysis_results, f, ensure_ascii=False, indent=4)
            self.logger.info(f"pass {self.name} 分析结果已保存到 {save_path}")
        except Exception as e:
            self.logger.error(f"保存分析结果失败: {e}", exc_info=True)
            raise RuntimeError(f"保存分析结果失败: {e}")
        
    def run(self,output_path: Optional[str] = None) -> None:
        """执行Pass分析"""
        self.logger.info(f"开始执行 {self.name} Pass")
        self.find_potential_target()
        self.confirm_potential()  # 确认潜在的source、sink和sanitizer
        self.logger.info(f"找到 {len(self.sources)} 个源函数，{len(self.sinks)} 个汇聚点函数，{len(self.sanitizers)} 个清理函数")
        self.logger.info(f"源函数列表: {[source.full_name for source in self.sources]}")
        self.logger.info(f"汇聚点函数列表: {[sink.full_name for sink in self.sinks]}")
        self.logger.info(f"清理函数列表: {[sanitizer.full_name for sanitizer in self.sanitizers]}")
        self.taint_analysis()
        self.vuln_analysis()
        self._save_results(output_path)
        return self.get_analysis_results()





