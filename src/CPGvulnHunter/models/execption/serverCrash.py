"""
Joern相关的自定义异常类
"""

class JoernException(Exception):
    """Joern相关异常的基类"""
    pass

class JoernServerCrashedException(JoernException):
    """Joern服务器崩溃异常"""
    def __init__(self, message: str, consecutive_timeouts: int = 0):
        super().__init__(message)
        self.consecutive_timeouts = consecutive_timeouts

class JoernTimeoutException(JoernException):
    """Joern命令超时异常"""
    def __init__(self, message: str, command: str, timeout_duration: int = 0):
        super().__init__(message)
        self.command = command
        self.timeout_duration = timeout_duration

class JoernConnectionException(JoernException):
    """Joern连接异常"""
    pass

class JoernCommandFailedException(JoernException):
    """Joern命令执行失败异常"""
    def __init__(self, message: str, command: str):
        super().__init__(message)
        self.command = command