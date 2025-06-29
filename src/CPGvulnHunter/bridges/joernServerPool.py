import threading
import queue
import time
import subprocess
import atexit
from typing import Dict, Optional, List
from dataclasses import dataclass
from pathlib import Path

from CPGvulnHunter.utils.threadLogger import get_thread_logger
from CPGvulnHunter.core.config import ConfigManager

@dataclass
class JoernServerInfo:
    """Joern服务器信息"""
    port: int
    process: subprocess.Popen
    is_available: bool = True
    last_used: float = 0.0
    error_count: int = 0

class JoernServerPool:
    """Joern服务器池管理器 - 单例模式"""
    
    _instance = None
    _lock = threading.Lock()
    _initialized = False
    
    def __new__(cls):
        """单例模式实现"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """初始化方法 - 只执行一次"""
        if self._initialized:
            return
            
        with self._lock:
            if self._initialized:
                return
                
            # 从配置获取Joern路径
            self.joern_config = ConfigManager.get_joern_config()
            self.joern_path = self.joern_config.installation_path
            
            # 默认配置
            self.server_number:int = 0
            
            # 服务器池
            self.servers: Dict[int, JoernServerInfo] = {}
            self.available_servers = queue.Queue()
            
            # 线程安全锁（实例级别的锁）
            self.pool_lock = threading.RLock()
            
            # 端口管理
            self.port_range_start = 9000
            self.port_range_end = 10000
            self.used_ports = set()
            
            self.logger = get_thread_logger()
            
            # 注册退出时的清理函数
            atexit.register(self.shutdown)
            
            # 标记为已初始化
            self._initialized = True
            
            self.logger.info("JoernServerPool单例实例创建完成")
    
    def configure(self, server_number: int = 10, 
                  port_start: int = 9000, port_end: int = 10000):
        """配置服务器池参数"""
        with self.pool_lock:
            if self.servers:
                self.logger.warning("服务器池已有运行的服务器，配置更改可能不会立即生效")
                
            self.server_number = server_number
            self.port_range_start = port_start
            self.port_range_end = port_end
            
            self.logger.info(f"服务器池配置更新: 服务器数量={server_number},  端口范围={port_start}-{port_end}")
    
    def start_pool(self):
        """启动服务器池（延迟初始化）"""
        with self.pool_lock:
            if not self.servers:
                self.logger.info("开始初始化服务器池")
                self._initialize_servers()
            else:
                self.logger.info("服务器池已启动，跳过初始化")
    
    def _find_free_port(self) -> Optional[int]:
        """查找空闲端口"""
        import socket
        for port in range(self.port_range_start, self.port_range_end):
            if port in self.used_ports:
                continue
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.bind(('localhost', port))
                    return port
            except OSError:
                continue
        return None
    
    def _start_joern_server(self, port: int) -> Optional[subprocess.Popen]:
        """启动单个Joern服务器"""
        try:
            cmd = [self.joern_path, "--server", "--server-port", str(port)]
            self.logger.info(f"启动Joern服务器命令: {' '.join(cmd)}")
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # 等待服务器启动
            time.sleep(5)  # 增加等待时间
            
            if process.poll() is None:  # 进程仍在运行
                self.logger.info(f"Joern服务器启动成功 - 端口: {port}, PID: {process.pid}")
                return process
            else:
                stdout, stderr = process.communicate()
                self.logger.error(f"Joern服务器启动失败 - 端口: {port}")
                self.logger.error(f"STDOUT: {stdout}")
                self.logger.error(f"STDERR: {stderr}")
                return None
        except Exception as e:
            self.logger.error(f"启动Joern服务器异常 - 端口: {port}, 错误: {e}", exc_info=True)
            return None
    
    def _initialize_servers(self):
        """初始化最小数量的服务器"""
        success_count = 0
        for i in range(self.server_number):
            if self._add_server():
                success_count += 1
            else:
                self.logger.warning(f"初始化第{i+1}个服务器失败")
        
        self.logger.info(f"服务器池初始化完成，成功启动 {success_count}/{self.server_number} 个服务器")
    
    def _add_server(self) -> bool:
        """添加新的服务器到池中"""
        port = self._find_free_port()
        if not port:
            self.logger.error("无法找到空闲端口")
            return False
        
        process = self._start_joern_server(port)
        if not process:
            return False
        
        server_info = JoernServerInfo(port=port, process=process)
        self.servers[port] = server_info
        self.used_ports.add(port)
        self.available_servers.put(port)
        
        self.logger.info(f"服务器池添加新服务器 - 端口: {port}, 当前总数: {len(self.servers)}")
        return True
    
    def get_server(self, timeout: float = 30.0) -> Optional[int]:
        """从池中获取可用服务器"""
        try:
            # 尝试从可用队列获取
            port = self.available_servers.get(timeout=timeout)
            
            with self.pool_lock:
                if port in self.servers:
                    server_info = self.servers[port]
                    if server_info.process.poll() is None and self.check_server(port=port):  # 进程仍在运行
                        server_info.is_available = False
                        server_info.last_used = time.time()
                        self.logger.debug(f"分配服务器 - 端口: {port}")
                        return port
                    else:
                        # 服务器进程已死亡，重启
                        self.logger.warning(f"服务器进程已死亡，尝试重启 - 端口: {port}")
                        if self.restart_server(port):
                            return self.get_server(timeout=timeout)  # 递归获取
                        else:
                            self.logger.error(f"无法重启服务器 - 端口: {port}")
                            return None
        except queue.Empty:
            self.logger.warning("没有可用服务器，阻塞等待中...")
            # 阻塞等待直到有服务器归还
            port = self.available_servers.get()  # 阻塞等待
            return self.get_server(timeout=timeout)
    
    def check_server(self, port: int) -> bool:
        """检查指定端口的服务器是否正常运行"""
        import socket
        try:
            with socket.create_connection(("localhost", port), timeout=5) as sock:
                self.logger.debug(f"服务器正常运行 - 端口: {port}")
                return True
        except (socket.timeout, ConnectionRefusedError) as e:
            self.logger.error(f"服务器不可用 - 端口: {port}, 错误: {e}")
            return False

    def return_server(self, port: int):
        """归还服务器到池中"""
        with self.pool_lock:
            if port in self.servers:
                server_info = self.servers[port]
                server_info.is_available = True
                self.available_servers.put(port)
                self.logger.debug(f"归还服务器 - 端口: {port}")
            else:
                self.logger.warning(f"尝试归还不存在的服务器 - 端口: {port}")
    
    def restart_server(self, port: int) -> bool:
        """重启指定端口的服务器"""
        if port not in self.servers:
            return False
            
        old_server = self.servers[port]
        
        # 终止旧进程
        try:
            old_server.process.terminate()
            old_server.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.logger.warning(f"服务器进程 {port} 终止超时，强制杀死")
            old_server.process.kill()
        except Exception as e:
            self.logger.error(f"终止服务器进程 {port} 异常: {e}", exc_info=True)
        
        # 启动新进程
        new_process = self._start_joern_server(port)
        if new_process:
            self.servers[port] = JoernServerInfo(port=port, process=new_process)
            self.available_servers.put(port)
            self.logger.info(f"服务器重启成功 - 端口: {port}")
            return True
        else:
            # 重启失败，从池中移除
            del self.servers[port]
            self.used_ports.discard(port)
            self.logger.error(f"服务器重启失败 - 端口: {port}")
            return False
    
    def shutdown(self):
        """关闭所有服务器"""
        if not self._initialized:
            return
            
        with self.pool_lock:
            self.logger.info("开始关闭所有Joern服务器")
            
            for port, server_info in self.servers.items():
                try:
                    self.logger.debug(f"正在关闭服务器 - 端口: {port}")
                    server_info.process.terminate()
                    server_info.process.wait(timeout=5)
                    self.logger.debug(f"服务器关闭成功 - 端口: {port}")
                except subprocess.TimeoutExpired:
                    self.logger.warning(f"服务器 {port} 关闭超时，强制杀死")
                    server_info.process.kill()
                except Exception as e:
                    self.logger.error(f"关闭服务器 {port} 异常: {e}", exc_info=True)
            
            self.servers.clear()
            self.used_ports.clear()
            
            # 清空队列
            while not self.available_servers.empty():
                try:
                    self.available_servers.get_nowait()
                except queue.Empty:
                    break
            
            self.logger.info("所有Joern服务器已关闭")
    
    def get_pool_status(self) -> Dict:
        """获取服务器池状态"""
        with self.pool_lock:
            total_servers = len(self.servers)
            available_count = self.available_servers.qsize()
            active_count = total_servers - available_count
            
            # 检查进程状态
            alive_servers = []
            dead_servers = []
            for port, server_info in self.servers.items():
                if server_info.process.poll() is None:
                    alive_servers.append(port)
                else:
                    dead_servers.append(port)
            
            return {
                "total_servers": total_servers,
                "available_servers": available_count,
                "active_servers": active_count,
                "alive_servers": len(alive_servers),
                "dead_servers": len(dead_servers),
                "max_servers": self.max_servers,
                "ports": list(self.servers.keys()),
                "alive_ports": alive_servers,
                "dead_ports": dead_servers
            }
    
    def health_check(self) -> bool:
        """健康检查"""
        with self.pool_lock:
            if not self.servers:
                return False
            
            alive_count = 0
            for port, server_info in self.servers.items():
                if server_info.process.poll() is None:
                    alive_count += 1
            
            health_ratio = alive_count / len(self.servers)
            is_healthy = health_ratio >= 0.5  # 至少50%的服务器存活
            
            self.logger.debug(f"健康检查: {alive_count}/{len(self.servers)} 个服务器存活, 健康状态: {is_healthy}")
            return is_healthy

    @classmethod
    def get_instance(cls, server_number: int = 8):
        """获取单例实例，并支持动态传参"""
        instance = cls.__new__(cls)  # 确保实例已创建
        if not instance._initialized:
            instance.__init__()  # 显式调用 __init__
        return instance

    def __del__(self):
        """析构函数"""
        self.shutdown()