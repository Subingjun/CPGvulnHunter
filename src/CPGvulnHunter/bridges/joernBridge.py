# -*- coding: utf-8 -*-
import asyncio
import subprocess
from typing import Optional, List, Dict, Any, Union, Tuple
from dataclasses import dataclass
import os
import re
import json
import logging
import time
import threading
import socket
import traceback
# import psutil  # 可选依赖，如果没有安装就使用替代方案
from cpgqls_client import CPGQLSClient

from CPGvulnHunter.bridges.joernServerPool import JoernServerPool
from CPGvulnHunter.core.config import ConfigManager, JoernConfig
from CPGvulnHunter.models.execption.serverCrash import JoernTimeoutException
from CPGvulnHunter.utils.threadLogger import get_thread_logger
from CPGvulnHunter.utils.threadLogger import get_thread_logger

class JoernBridge:
    def __init__(self) -> None:
        self.logger = get_thread_logger()
        # 先初始化所有实例属性，保证异常时析构安全
        self.joern_server_pool: JoernServerPool = JoernServerPool.get_instance()
        self.server_port :int = self.joern_server_pool.get_server()
        self.server_endpoint: str = "localhost:" + str(self.server_port)
        self.joern_cmd_history = []
        self._last_activity = time.time()
        self._client = None
        self._loop = None
        self.timeout = 60
        self.server_endpoint = str('localhost') + ':' + str(self.server_port)
        #self._setup_and_start_server() joern server should initialize by engine
        self._client = CPGQLSClient(
                server_endpoint=self.server_endpoint,
                event_loop=self._loop
            )
        self._test_connect()
    
    def __del__(self) -> None:
        try:
            self._cleanup_server()
        except:
            pass
    
    def _test_connect(self) -> None:
        """测试连接到Joern服务器"""
        try:
            test_result = self._client.execute("val testConnection = 1")
            if test_result.get('success', False):
                self._connected = True
                self._last_activity = time.time()
                self.logger.info("成功连接到Joern服务器")
            else:
                raise RuntimeError(f"服务器连接测试失败: {test_result}")
        except Exception as e:
            self.logger.error(f"连接Joern服务器失败: {e}\n{traceback.format_exc()}")
            self._connected = False
            raise RuntimeError(f"无法连接到Joern服务器: {e}")


#===================================================export methods=======================================================================
    def send_command(self, cmd: str) -> str | None:
        for retry_count in range(3):
            self.joern_cmd_history.append(cmd)

            timestamp = time.time()
            os.makedirs('logs', exist_ok=True)
            with open('logs/joern_command_history.log', 'a', encoding='utf-8') as f:
                f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))}] {cmd}\n")

            try:
                self._ensure_connection()
                response = self._execute_with_timeout(cmd, self.timeout)
                
                self._last_activity = time.time()
                self._consecutive_timeouts = 0
                if response is not None:
                    output = self._parse_server_response(response)
                    self.logger.debug(f"命令 {cmd} 执行成功")
                    return output
                else:
                    self.logger.warning(f"命令执行返回空结果: {cmd}")
                    if retry_count >= 2:
                        return None
                    continue
                    
            except TimeoutError as e:
                self.logger.error(f"命令执行超时: {cmd}, 错误: {e}\n{traceback.format_exc()}")
                self.logger.info("执行服务器健康检测...")
                health_check_result = self.health_check()
                if not health_check_result:
                    self.logger.error(f"Joern server{self.server_endpoint} 宕机，尝试重启Joern server并恢复上下文")
                    try:
                        self._solve_server_crash()
                    except Exception as crash_e:
                        self.logger.error(f"服务器恢复失败: {crash_e}\n{traceback.format_exc()}")
                        if retry_count >= 2:
                            return None
                        continue
                else:
                    self.logger.info("Joern服务器正常，尝试重新执行命令")
                    continue
            except Exception as e:
                self.logger.error(f"执行命令时发生未知错误: {e}\n{traceback.format_exc()}")
                if retry_count >= 2:  # 最后一次重试
                    return None
                continue
        
        # 如果所有重试都失败，返回 None
        self.logger.error(f"命令执行失败，已用尽所有重试次数: {cmd}")
        return None

    def health_check(self) -> bool:
        """
        检查服务器健康状态
        
        Returns:
            True if healthy, False otherwise
        """
        try:
            # 直接使用客户端执行命令，避免递归调用 send_command
            if not self._client:
                return False
                
            result = self._client.execute("1 + 1")
            if result and result.get('success', False):
                stdout = result.get('stdout', '')
                return "2" in stdout
            return False
        except Exception as e:
            self.logger.warning(f"健康检查失败: {e}\n{traceback.format_exc()}")
            return False

    #===================================================private methods=======================================================================

    def _execute_with_timeout(self, cmd: str, timeout: int) -> Dict[str, Any] | None:
        """
        使用超时机制执行命令，优化版本
        
        Args:
            cmd: 要执行的命令
            timeout: 超时时间（秒）
            
        Returns:
            命令执行结果
            
        Raises:
            TimeoutError: 执行超时
            RuntimeError: 执行失败
        """
        import concurrent.futures
        import threading
        
        def execute_command():
            """内部执行函数"""
            try:
                if not self._client:
                    raise RuntimeError("客户端连接未初始化")
                
                self.logger.debug(f"开始执行命令: {cmd[:100]}...")
                result = self._client.execute(cmd)
                self.logger.debug(f"命令执行完成")
                return result
            except Exception as e:
                self.logger.error(f"执行命令时出错: {e}\n{traceback.format_exc()}")
                raise
        
        result_container: List[Any] = [None]
        exception_container: List[Optional[Exception]] = [None]
        completed_event = threading.Event()
        
        def worker():
            """工作线程函数"""
            try:
                result = execute_command()
                result_container[0] = result
            except Exception as e:
                exception_container[0] = e
            finally:
                completed_event.set()
        
        # 启动工作线程
        worker_thread = threading.Thread(target=worker, daemon=True)
        worker_thread.start()
        
        # 等待完成或超时
        if completed_event.wait(timeout=timeout):
            # 命令完成
            if exception_container[0] is not None:
                # 执行过程中出现异常
                raise RuntimeError(f"命令执行失败: {exception_container[0]}")
            return result_container[0]
        else:
            self.logger.error(f"命令执行超时 ({timeout}秒): {cmd[:100]}...")
            raise TimeoutError(f"命令执行超时({timeout}s): {cmd[:50]}...")
   


    def _solve_server_crash(self) -> None:
        """
        处理服务器崩溃情况，尝试重启服务器并恢复上下文
        """
        try:
            self.logger.info("尝试重启Joern服务器...")
            joern_server_pool = JoernServerPool().get_instance()
            # 从endpoint中提取端口号
            port = int(self.server_endpoint.split(':')[1])
            joern_server_pool.restart_server(port)
            # 重新连接
            self._test_connect()
            self.logger.info("Joern服务器已重启并重新连接")
        except Exception as e:
            self.logger.error(f"重启Joern服务器失败: {e}\n{traceback.format_exc()}")
            raise RuntimeError(f"无法恢复Joern服务器: {e}")

    def _setup_and_start_server(self) -> None:
        """启动joernserver"""
        try:
            # 解析server endpoint
            host, port_str = self.server_endpoint.split(':')
            port = int(port_str)
            
            # 如果端口被占用，先尝试关闭占用端口的进程
            if self._is_port_open(host, port):
                self.logger.info(f"检测到端口 {port} 已被占用，尝试关闭占用进程...")
                self._kill_process_on_port(port)
                
                # 等待端口释放
                max_wait = 10
                for i in range(max_wait):
                    if not self._is_port_open(host, port):
                        self.logger.info(f"端口 {port} 已释放")
                        break
                    time.sleep(1)
                else:
                    self.logger.warning(f"端口 {port} 仍被占用，强制启动新服务器")
            
            # 设置Java环境并启动服务器
            self.logger.info("启动新的Joern服务器...")
            self._setup_java_environment()
            
            if not self._start_joern_server():
                raise RuntimeError("启动Joern服务器失败")
                
        except Exception as e:
            self.logger.error(f"设置和启动服务器失败: {e}\n{traceback.format_exc()}")
            raise RuntimeError(f"无法启动Joern服务器: {e}")

    def _cleanup_server(self) -> None:
        """清理服务器资源"""
        try:
            # 关闭连接
            if self._client:
                self._client = None
                self._connected = False
            
            # 归还服务器到池中
            if  self.server_port:
                self.logger.info(f"归还服务器到池中: {self.server_port}")
                self.joern_server_pool.return_server(self.server_port)
        
            
        except Exception as e:
            self.logger.error(f"清理服务器资源时出错: {e}\n{traceback.format_exc()}")


    def _is_port_open(self, host: str, port: int) -> bool:
        """检查端口是否开放"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(2)
                result = sock.connect_ex((host, port))
                return result == 0
        except Exception:
            return False

    def _kill_process_on_port(self, port: int) -> None:
        """终止占用指定端口的进程"""
        try:
            # 使用lsof命令查找占用端口的进程
            result = subprocess.run(
                ['lsof', '-ti', f':{port}'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0 and result.stdout.strip():
                pids = result.stdout.strip().split('\n')
                for pid in pids:
                    if pid.strip():
                        try:
                            self.logger.info(f"终止进程 PID: {pid}")
                            subprocess.run(['kill', '-9', pid], timeout=5)
                        except Exception as e:
                            self.logger.warning(f"无法终止进程 {pid}: {e}\n{traceback.format_exc()}")
            else:
                self.logger.info(f"未找到占用端口 {port} 的进程")
                
        except subprocess.TimeoutExpired:
            self.logger.warning("查找端口占用进程超时")
        except FileNotFoundError:
            # lsof命令不存在，尝试使用netstat + ps
            try:
                self._kill_process_on_port_fallback(port)
            except Exception as e:
                self.logger.warning(f"无法终止端口 {port} 的占用进程: {e}\n{traceback.format_exc()}")
        except Exception as e:
            self.logger.warning(f"终止端口占用进程时出错: {e}\n{traceback.format_exc()}")

    def _kill_process_on_port_fallback(self, port: int) -> None:
        """备用方法：使用netstat查找并终止占用端口的进程"""
        try:
            # 使用netstat查找进程
            result = subprocess.run(
                ['netstat', '-tlnp'], 
                capture_output=True, 
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if f':{port} ' in line and 'LISTEN' in line:
                        # 提取PID
                        parts = line.split()
                        if len(parts) >= 7:
                            pid_part = parts[6]  # 格式通常是 PID/程序名
                            if '/' in pid_part:
                                pid = pid_part.split('/')[0]
                                if pid.isdigit():
                                    try:
                                        self.logger.info(f"终止进程 PID: {pid}")
                                        subprocess.run(['kill', '-9', pid], timeout=5)
                                    except Exception as e:
                                        self.logger.warning(f"无法终止进程 {pid}: {e}\n{traceback.format_exc()}")
        except Exception as e:
            self.logger.warning(f"备用终止方法失败: {e}\n{traceback.format_exc()}")

    def _setup_java_environment(self) -> None:
        """设置Java环境变量，增加堆空间和内存"""
        java_opts = [
            "-Xmx8G",           # 最大堆内存8GB
            "-Xms2G",           # 初始堆内存2GB
            "-Xss8m",           # 栈大小8MB
            "-XX:+UseG1GC",     # 使用G1垃圾收集器
            "-XX:MaxGCPauseMillis=200",  # GC暂停时间
            "-XX:+UnlockExperimentalVMOptions",
            "-XX:+UseContainerSupport",  # 容器支持
            "-XX:MaxRAMPercentage=75.0"  # 最大RAM使用百分比
        ]
        
        # 设置环境变量
        current_java_opts = os.environ.get('JAVA_OPTS', '')
        new_java_opts = ' '.join(java_opts)
        
        os.environ['JAVA_OPTS'] = f"{current_java_opts} {new_java_opts}".strip()
        os.environ['_JAVA_OPTIONS'] = new_java_opts
        
        self.logger.info(f"设置JVM参数: {new_java_opts}")



    def _is_connected(self) -> bool:
        """检查是否连接到服务器"""
        return self._connected and self._client is not None

    def _ensure_connection(self) -> None:
        """确保连接可用，如果断开则重连"""
        if not self._is_connected():
            self.logger.warning("检测到连接断开，尝试重新连接")
            self._test_connect()

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
        
        # 清理前导和尾随空格
        clean_output = clean_output.strip()
        
        return clean_output

    def _parse_server_response(self, response: Dict[str, Any]) -> str | None:
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
        
        return ""
