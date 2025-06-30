from CPGvulnHunter.bridges.joernServerPool import JoernServerPool
from CPGvulnHunter.bridges.joernWrapper import JoernWrapper
from CPGvulnHunter.bridges.llmWrapper import LLMWrapper
from CPGvulnHunter.core.config import ConfigManager
from CPGvulnHunter.core.cpg import CPG


class MockCpg:
    def __init__(self):
        #初始化joern之前，必须要初始化joern server pool
        ConfigManager.initialize("/home/nstl/data/CPGvulnHunter/config.yml")
        self._init_joern_server_pool()
        self.joern_wrapper = JoernWrapper()
        self.llm_wrapper = LLMWrapper()
        self.taget_src_path = "/home/nstl/data/CPGvulnHunter/test/test_case/test4/CWE78_OS_Command_Injection__char_connect_socket_execl_01"
        self.cpg = CPG(self.taget_src_path, self.llm_wrapper, self.joern_wrapper)

    def _init_joern_server_pool(self):
        self.joern_server_pool = JoernServerPool.get_instance()
        # 有多少个线程，就开多少个服务器。
        self.joern_server_pool.configure(server_number=1)
        self.joern_server_pool.start_pool()
    


