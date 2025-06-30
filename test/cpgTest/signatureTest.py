import subprocess
from CPGvulnHunter.bridges.joernServerPool import JoernServerPool
from CPGvulnHunter.bridges.joernWrapper import JoernWrapper
from CPGvulnHunter.bridges.llmWrapper import LLMWrapper
from CPGvulnHunter.core.cpg import CPG
from CPGvulnHunter.utils.threadLogger import get_thread_logger
from cpg_mock import MockCpg


class signatureTest:
    def __init__(self):
        #初始化joern之前，必须要初始化joern server pool
        self.cpg = MockCpg().cpg
    

    def test_signature(self):
        """
        测试函数签名生成
        """
        self.run_netstat()

        for func in self.cpg.functions:
            signature = func.get_full_signature()
            print(f" {signature}")
            assert signature is not None, f"Function {func.name} signature should not be None"
            assert isinstance(signature, str), f"Function {func.name} signature should be a string"
        print("清理测试")
        self.run_netstat()
        
    def run_netstat(self):
        """运行 netstat -tunlp 命令并打印日志"""
        logger = get_thread_logger()

        try:
            logger.info("开始运行 netstat -tunlp 命令...")
            # 运行 netstat 命令
            result = subprocess.run(
                ["netstat", "-tunlp"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # 检查命令是否成功
            if result.returncode == 0:
                logger.info("netstat 命令运行成功")
                logger.info(f"命令输出:\n{result.stdout}")
            else:
                logger.error(f"netstat 命令运行失败，错误码: {result.returncode}")
                logger.error(f"错误信息:\n{result.stderr}")
        except Exception as e:
            logger.error(f"运行 netstat 命令时发生异常: {e}", exc_info=True)

if __name__ == "__main__":
     signatureTest().test_signature()