import os
from pathlib import Path
from CPGvulnHunter.core.engine import VulnerabilityEngine



class BatchTestCWE78:
    """
    批量测试CWE-78漏洞检测
    """
    
    def __init__(self, config_file: str):
        self.config_file=config_file
        self.src_path = "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/output/CWE78_OS_Command_Injection/s01"
        self.testcase_dirs = self.get_test_directories_full_paths()
        self.vuln_functions = {}

    def run(self):
        for testcase_dir in self.testcase_dirs:
            print(f"正在分析测试目录: {testcase_dir}")
            # 先把所有的分析结果加到vuln_function字典中
            try:
                engine = VulnerabilityEngine(self.config_file)
                result = engine.run(src_path=testcase_dir, passes=["cwe78"])
                a = result.get("cwe78", {})
                analysis_results :list = result.get("cwe78", {}).get('analysis_results', {})
                for result in analysis_results:
                    is_vulnerable = result.get('is_vulnerable')
                    confidence = result.get('confidence')
                    reason = result.get('reason')
                    vuln_function_name = result.get('vuln_function_name')
                    if is_vulnerable:
                        self.vuln_functions[vuln_function_name] = {
                            "confidence": confidence,
                            "reason": reason
                        }
            except Exception as e:
                print(f"分析失败: {e}")
                continue
        #计算结果的正确率
        correct_count = 0
        total_count = len(self.vuln_functions)
        wrong_count = 0
        for vuln_function_name, details in self.vuln_functions.items():
            is_correct = self.checkAnswer(vuln_function_name)
            if is_correct:
                correct_count += 1
            else:
                wrong_count += 1
        
        result = {
            "total_count": total_count,
            "correct_count": correct_count,
            "wrong_count": wrong_count,
            "tp_rate": correct_count / total_count if total_count > 0 else 0,
            "fp_rate": wrong_count / total_count if total_count > 0 else 0,
            "vuln_functions": self.vuln_functions
        }
        print(f"分析完成: {result}")


    def checkAnswer(self, vuln_function_name: str):
        """
        判断漏洞函数是否正确：
        如果函数名中包含bad则说明正确，如果不包含则说明不正确
        """
        if "bad" in vuln_function_name:
            return True
        else:
            False

    def get_test_directories_full_paths(self):
        """
        获取测试目录下所有子目录的完整路径列表
        
        Returns:
            list: 子目录完整路径列表
        """
        test_dir = Path(self.src_path)
        if not test_dir.exists():
            print(f"目录不存在: {test_dir}")
            return []
        
        # 获取所有子目录的完整路径
        subdirs = [
            str(item) for item in test_dir.iterdir() 
            if item.is_dir() and not item.name.startswith('.')
        ]
        
        # 按名称排序
        subdirs.sort()
        
        return subdirs

if __name__ == "__main__":
    BatchTestCWE78(config_file="config.yml").run()