

class JoernServerManager:
    """
    在程序启动的时候维护一个joern的进程池，标记了每一个joern的端口
    负责启动和停止joern服务器
    """

    def __init__(self, server_path: str):
        self.server_path = server_path

    def start_server(self):
        """
        Start the Joern server.
        """
        print(f"Starting Joern server at {self.server_path}...")

    def stop_server(self):
        """
        Stop the Joern server.
        """
        print("Stopping Joern server...")