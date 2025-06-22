from typing import Optional, List, Dict, Any, Union, Tuple
from dataclasses import dataclass
import os
import re
import json
import logging
import time
import threading
from cpgqls_client import CPGQLSClient

from CPGvulnHunter.core.config import ConfigManager, JoernConfig

class JoernBridge:
    """
    与 Joern 服务器交互的桥接类（server-based版本）
    使用 cpgqls_client 与 Joern 服务器通信，替代原有的 pexpect shell 交互
    """
    
    def __init__(self, joern_path: str = "joern", timeout: int = 120, 
                 server_endpoint: str = "localhost:8080", 
                 auth_credentials: Optional[Tuple[str, str]] = None) -> None:
        """
        直接从config中获取Joern配置
        """
        self.joern_config:JoernConfig = ConfigManager().get_joern_config()
        self.joern_path: str = self.joern_config.installation_path  # 保留为了兼容性
        self.timeout: int = self.joern_config.timeout
        self.server_endpoint: str = self.joern_config.server_endpoint
        self._connected: bool = False
        self.logger = logging.getLogger(__name__)
        self._init_joern_server()
        self._command_history= []  # 存储命令历史
 



    def _init_joern_server(self) -> None:
        """
        建立与Joern服务器的连接
        """
        try:
            self.logger.info(f"连接到Joern服务器: {self.server_endpoint}")
            
            # 创建客户端连接
            self._client = CPGQLSClient(
                server_endpoint=self.server_endpoint,
            )
            
            # 测试连接
            test_result = self._client.execute("val testConnection = 1")
            if test_result.get('success', False):
                self._connected = True
                self._last_activity = time.time()
                self.logger.info("成功连接到Joern服务器")
            else:
                raise RuntimeError(f"服务器连接测试失败: {test_result}")
                
        except Exception as e:
            self.logger.error(f"连接Joern服务器失败: {e}")
            self._connected = False
            raise RuntimeError(f"无法连接到Joern服务器: {e}")

    def close_shell(self) -> None:
        """
        关闭与Joern服务器的连接
        """
        try:
            if self._client:
                self.logger.info("关闭Joern服务器连接")
                # cpgqls_client 通常自动管理连接
                self._client = None
                self._connected = False
        except Exception as e:
            self.logger.error(f"关闭连接时出错: {e}")

    def _is_connected(self) -> bool:
        """检查是否连接到服务器"""
        return self._connected and self._client is not None

    def _ensure_connection(self) -> None:
        """确保连接可用，如果断开则重连"""
        if not self._is_connected():
            self.logger.warning("检测到连接断开，尝试重新连接")
            self._init_joern_server()

    def _clean_output(self, raw_output: str) -> str:
        """
        清理服务器输出，模拟原有的shell输出清理逻辑
        
        Args:
            raw_output: 服务器返回的原始输出
            
        Returns:
            清理后的输出字符串
        """
        if not raw_output:
            return ""
        
        # 移除ANSI转义码（颜色代码等）
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        clean_output = ansi_escape.sub('', raw_output)
        
        # 移除其他控制字符
        control_chars = re.compile(r'[\r\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]+')
        clean_output = control_chars.sub('', clean_output)
        
        # 移除多余的换行符
        clean_output = re.sub(r'\n{2,}', '\n', clean_output)
        
        # 清理前导和尾随空白
        clean_output = clean_output.strip()
        
        return clean_output

    def _parse_server_response(self, response: Dict[str, Any]) -> str|None:
        """
        解析服务器响应，提取输出内容
        
        Args:
            response: 服务器返回的响应字典
            
        Returns:
            提取的输出字符串
            
        Raises:
            RuntimeError: 如果响应表示执行失败
        """
        if not response:
            return ""
        
        success = response.get('success', False)
        if not success:
            error_msg = response.get('stderr', response.get('message', '未知错误'))
            self.logger.error(f"命令执行失败: {error_msg}")
            return None
        # 提取标准输出
        stdout = response.get('stdout', '')
        if stdout:
            return self._clean_output(stdout)

    def send_command(self, cmd: str, timeout: Optional[int] = None) -> str |None:
        """
        发送命令到Joern服务器并返回输出
        
        Args:
            cmd: 要执行的命令
            timeout: 命令超时时间（秒），默认使用实例超时时间
            
        Returns:
            命令输出字符串
            
        Raises:
            RuntimeError: 命令执行失败或超时
        """
        if not cmd.strip():
            return ""
        
        # 记录命令历史
        timestamp = time.time()
        self._command_history.append({
            'command': cmd,
            'timestamp': timestamp
        })
        
        # 记录到日志文件
        os.makedirs('logs', exist_ok=True)
        with open('logs/joern_command_history.log', 'a', encoding='utf-8') as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))}] {cmd}\n")
        
        # 保持最近100条命令
        if len(self._command_history) > 100:
            self._command_history = self._command_history[-100:]
            
        try:
            # 确保连接可用
            self._ensure_connection()
            
            if not self._client:
                raise RuntimeError("无法建立或维持Joern服务器连接")
            
            # 执行命令
            response = self._client.execute(cmd)
            self._last_activity = time.time()
            
            if response is None:
                self.logger.error("服务器响应为空，可能是连接问题或命令错误")
            # 解析响应
            output = self._parse_server_response(response)
            return output
                
        except Exception as e:
            self.logger.error(f"命令执行出错: {e}")
            raise RuntimeError(f"命令执行失败: {e}")

   

    def health_check(self) -> bool:
        """
        健康检查：验证Joern服务器是否正常工作
        
        Returns:
            True if healthy, False otherwise
        """
        try:
            # 发送简单的测试命令
            result = self.send_command("1 + 1", timeout=10)
            return "2" in result and not result.strip() == "=~"
        except Exception as e:
            self.logger.warning(f"健康检查失败: {e}")
            return False

    def get_status(self) -> Dict[str, Any]:
        """
        获取桥接器状态信息
        
        Returns:
            包含状态信息的字典
        """
        return {
            "connected": self._is_connected(),
            "server_endpoint": self.server_endpoint,
            "timeout": self.timeout,
            "last_activity": self._last_activity,
            "uptime": time.time() - self._last_activity if self._is_connected() else 0,
            "command_count": len(self._command_history),
            "connection_type": "server"  # 标识这是server版本
        }

    def get_command_history(self) -> List[Dict[str, Any]]:
        """获取命令历史"""
        return self._command_history.copy()

    def __del__(self) -> None:
        """析构函数，确保资源清理"""
        try:
            self.close_shell()
        except:
            pass
