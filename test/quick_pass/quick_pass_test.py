from CPGvulnHunter.passes.quickPass import QuickPass
from cpg_mock import MockCpg


class QuickPassTest():
    """
    测试快速通过
    """
    def __init__(self):
        """
        初始化函数
        """
        print("开始快速通过测试")
        self.cpg = MockCpg().cpg
        self.qp = QuickPass(cpg=self.cpg)
   
    def run(self):
        result  = self.qp.find_potential_target()
        print("快速通过测试结果:")
        print(result)
        print(len(self.qp.sources))
        print(len(self.qp.sinks))
        print(len(self.qp.sanitizers))
        self.qp.confirm_potential()
        self.qp.taint_analysis()
        self.qp.vuln_analysis()
        self.qp._save_results("/home/nstl/data/CPGvulnHunter/test/quick_pass/log")

if __name__ == "__main__":
    qp_test = QuickPassTest()
    qp_test.run()
    print("快速通过测试完成")