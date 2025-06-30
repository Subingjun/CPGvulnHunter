from CPGvulnHunter.core.cpg import CPG
from CPGvulnHunter.models.llm.dataclass import LLMRequest
from CPGvulnHunter.utils.threadLogger import get_thread_logger



class EasyPass:
    """
    EasyPass - 一个简单的pass，利用LLM分析函数是否存在安全风险
    该pass不依赖于复杂的污点分析或数据流分析，而是直接利用LLM对函数进行分析
    """

    def __init__(self, cpg:CPG):
        """
        :param cpg: CPG对象
        """
        self.cpg:CPG = cpg
        self.logger = get_thread_logger()
        self.vulnerabilitiesResults = []  # 存储漏洞分析结果

    def run(self,output_path="./easy_results"):
        """执行EasyPass"""
        self.logger.info("开始执行EasyPass")
        self.analyze_functions(output_path)
        return self.vulnerabilitiesResults

    def analyze_functions(self, output_path="./easy_results"):
        """对所有函数进行安全风险分析"""
        if not self.cpg.llm_wrapper:
            self.logger.error("LLM wrapper未初始化，无法执行函数分析")
            return None

        # 统计信息
        total_functions = len(self.cpg.internal_functions)
        vulnerable_count = 0
        attack_surface_count = 0
        
        self.logger.info(f"开始分析 {total_functions} 个内部函数")
        
        # 准备输出文件路径
        if output_path:
            from pathlib import Path
            output_dir = Path(output_path)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            vulnerable_file = output_dir / "vulnerable_functions.json"
            attack_surface_file = output_dir / "attack_surface_functions.json"
            summary_file = output_dir / "analysis_summary.json"
        
        for i, function in enumerate(self.cpg.internal_functions, 1):
            try:
                self.logger.info(f"正在分析函数 [{i}/{total_functions}]: {function.full_name}")
                
                request = self.build_function_analysis_request(function)
                llm_result = self.cpg.llm_wrapper.analyze_function(request)
                
                if llm_result and 'analysis_result' in llm_result:
                    analysis_result = self._parse_analysis_result(llm_result['analysis_result'])
                    
                    if analysis_result:
                        # 添加函数基本信息到结果中
                        analysis_result['function_name'] = function.full_name
                        analysis_result['file_location'] = f"{getattr(function, 'file_name', '未知文件')}:{getattr(function, 'line_number', '未知行号')}"
                        analysis_result['function_signature'] = function.get_full_signature() if hasattr(function, 'get_sigenature') else '签名不可用'
                        
                        # 判断是否为漏洞
                        is_vulnerable = analysis_result.get('is_vulnerable', False)
                        # 判断是否为攻击面
                        is_attack_surface = analysis_result.get('is_attack_surface', False)
                        
                        # 打印判断结果
                        self._print_analysis_result(function, analysis_result, is_vulnerable, is_attack_surface)
                        
                        # 如果是漏洞，加入漏洞结果列表并写入文件
                        if is_vulnerable:
                            self.vulnerabilitiesResults.append(analysis_result)
                            vulnerable_count += 1
                            
                            if output_path:
                                self._append_to_file(vulnerable_file, analysis_result, "漏洞函数")
                        
                        # 如果是攻击面，写入攻击面文件
                        if is_attack_surface:
                            attack_surface_count += 1
                            
                            if output_path:
                                self._append_to_file(attack_surface_file, analysis_result, "攻击面函数")
                        
                        # 如果既不是漏洞也不是攻击面
                        if not is_vulnerable and not is_attack_surface:
                            self.logger.info(f"✅ 函数 {function.full_name} 安全且非攻击面")
                    
                    else:
                        self.logger.warning(f"⚠️  函数 {function.full_name} 的LLM分析结果解析失败")
                else:
                    self.logger.warning(f"⚠️  函数 {function.full_name} 的LLM分析返回空结果")
                    
            except Exception as e:
                self.logger.error(f"❌ 分析函数 {function.full_name} 时出错: {e}", exc_info=True)
        
        # 输出最终统计信息
        self.logger.info(f"🎯 EasyPass分析完成:")
        self.logger.info(f"   - 总函数数: {total_functions}")
        self.logger.info(f"   - 漏洞函数: {vulnerable_count}")
        self.logger.info(f"   - 攻击面函数: {attack_surface_count}")
        self.logger.info(f"   - 安全函数: {total_functions - max(vulnerable_count, attack_surface_count)}")
        
        # 保存分析摘要
        if output_path:
            self._save_analysis_summary(summary_file, total_functions, vulnerable_count, attack_surface_count)

    def _print_analysis_result(self, function, analysis_result, is_vulnerable, is_attack_surface):
        """打印详细的分析结果"""
        function_name = function.full_name
        
        if is_vulnerable and is_attack_surface:
            # 既是漏洞又是攻击面 - 最危险
            severity = analysis_result.get('severity', 'Unknown')
            vuln_type = analysis_result.get('vulnerability_type', 'Unknown')
            attack_type = analysis_result.get('attack_surface_type', 'Unknown')
            self.logger.warning(f"🚨 函数 {function_name} - 高危险: 漏洞[{severity}] {vuln_type} + 攻击面[{attack_type}]")
            
        elif is_vulnerable:
            # 仅漏洞
            severity = analysis_result.get('severity', 'Unknown')
            vuln_type = analysis_result.get('vulnerability_type', 'Unknown')
            confidence = analysis_result.get('confidence', 0.0)
            self.logger.warning(f"🔴 函数 {function_name} - 存在漏洞: [{severity}] {vuln_type} (置信度: {confidence:.2f})")
            
        elif is_attack_surface:
            # 仅攻击面
            attack_type = analysis_result.get('attack_surface_type', 'Unknown')
            risk_level = analysis_result.get('risk_level', 'Unknown')
            self.logger.info(f"🟡 函数 {function_name} - 攻击面: [{risk_level}] {attack_type}")
            
        else:
            # 安全
            self.logger.debug(f"✅ 函数 {function_name} - 安全")

    def _parse_analysis_result(self, llm_response):
        """解析LLM返回的分析结果"""
        try:
            import json
            import re
            
            if isinstance(llm_response, str):
                # 尝试提取JSON部分
                json_match = re.search(r'\{.*\}', llm_response, re.DOTALL)
                if json_match:
                    json_str = json_match.group()
                    return json.loads(json_str)
                else:
                    self.logger.warning("LLM响应中未找到有效的JSON格式")
                    return None
            elif isinstance(llm_response, dict):
                return llm_response
            else:
                self.logger.warning(f"未知的LLM响应格式: {type(llm_response)}")
                return None
                
        except json.JSONDecodeError as e:
            self.logger.error(f"解析LLM JSON响应失败: {e}", exc_info=True)
            self.logger.debug(f"原始响应: {llm_response}")
            return None
        except Exception as e:
            self.logger.error(f"处理LLM响应时出错: {e}", exc_info=True)
            return None

    def _append_to_file(self, file_path, analysis_result, result_type):
        """追加模式写入分析结果到文件"""
        try:
            import json
            import os
            from datetime import datetime
            
            # 准备写入的数据
            record = {
                "timestamp": datetime.now().isoformat(),
                "type": result_type,
                "data": analysis_result
            }
            
            # 检查文件是否存在，如果不存在则创建
            if not os.path.exists(file_path):
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump([], f, ensure_ascii=False, indent=2)
            
            # 读取现有数据
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    existing_data = json.load(f)
                except json.JSONDecodeError:
                    existing_data = []
            
            # 追加新数据
            existing_data.append(record)
            
            # 写回文件
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, ensure_ascii=False, indent=2)
            
            self.logger.debug(f"已将{result_type}结果追加到: {file_path}")
            
        except Exception as e:
            self.logger.error(f"写入文件 {file_path} 时出错: {e}", exc_info=True)

    def _save_analysis_summary(self, summary_file, total_functions, vulnerable_count, attack_surface_count):
        """保存分析摘要"""
        try:
            import json
            from datetime import datetime
            
            summary = {
                "analysis_timestamp": datetime.now().isoformat(),
                "pass_name": "EasyPass",
                "statistics": {
                    "total_functions": total_functions,
                    "vulnerable_functions": vulnerable_count,
                    "attack_surface_functions": attack_surface_count,
                    "safe_functions": total_functions - max(vulnerable_count, attack_surface_count)
                },
                "vulnerability_rate": vulnerable_count / total_functions if total_functions > 0 else 0.0,
                "attack_surface_rate": attack_surface_count / total_functions if total_functions > 0 else 0.0
            }
            
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"分析摘要已保存到: {summary_file}")
            
        except Exception as e:
            self.logger.error(f"保存分析摘要失败: {e}", exc_info=True)

    def run(self, output_path=None):
        """执行EasyPass"""
        self.logger.info("开始执行EasyPass")
        self.analyze_functions(output_path)
        return self.vulnerabilitiesResults

    def build_function_analysis_request(self, function):
        """构建函数分析请求"""
        
        # 系统提示词 - 定义LLM的角色和任务
        sysprompt = """你是一个专业的代码安全分析专家，专门识别代码中的安全漏洞和攻击面。

你的主要任务包括两个方面：

1. 安全漏洞检测 - 识别以下类型的安全风险：
   - 缓冲区溢出（Buffer Overflow）
   - 命令注入（Command Injection）
   - SQL注入（SQL Injection）
   - 路径遍历（Path Traversal）
   - 格式字符串漏洞（Format String Vulnerability）
   - 空指针解引用（Null Pointer Dereference）
   - 内存泄漏（Memory Leak）
   - 整数溢出（Integer Overflow）
   - 未初始化变量使用（Use of Uninitialized Variable）
   - 竞态条件（Race Condition）
   - 其他类型的可能存在的安全风险

2. 攻击面分析 - 判断函数是否为攻击入口点：
   - 是否接收外部输入（网络输入、文件输入、用户输入等）
   - 是否为API端点或回调函数
   - 是否处理不可信数据
   - 是否为程序的入口函数

分析要求：
- 仔细检查每个危险函数调用和API使用
- 分析参数来源和数据流
- 识别潜在的攻击向量
- 评估函数的暴露程度和风险等级

请严格按照以下JSON格式返回分析结果：
{
    "is_vulnerable": true/false,
    "vulnerability_type": "具体漏洞类型或null",
    "severity": "Critical/High/Medium/Low或null",
    "vulnerability_description": "漏洞详细描述或null",
    "is_attack_surface": true/false,
    "attack_surface_type": "攻击面类型：网络输入/文件输入/用户输入/API端点/其他或null",
    "attack_surface_description": "攻击面描述或null",
    "risk_level": "High/Medium/Low",
    "confidence": 0.0-1.0
}

注意：即使没有发现漏洞，也要分析是否为攻击面。"""

        # 用户提示词 - 提供具体的函数信息
        userprompt = f"""请分析以下函数的安全性和攻击面：

函数基本信息：
- 函数名称: {function.full_name}
- 函数签名: {function.get_sigenature() if hasattr(function, 'get_sigenature') else '签名不可用'}

函数代码：
```c
{function.code}
```

请仔细分析：
1. 此函数是否存在安全漏洞？
2. 此函数是否构成攻击面（即是否接收或处理外部/不可信输入）？
3. 风险等级是什么？

请严格按照指定的JSON格式返回分析结果。"""

        request = LLMRequest(sysprompt, userprompt)
        return request