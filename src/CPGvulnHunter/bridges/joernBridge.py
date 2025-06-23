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
# import psutil  # 可选依赖，如果没有安装就使用替代方案
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
        # 首先初始化logger，因为其他方法都需要用到
        self.logger = logging.getLogger(__name__)
        
        try:
            self.joern_config: JoernConfig = ConfigManager().get_joern_config()
            self.joern_path: str = self.joern_config.installation_path if self.joern_config.installation_path else joern_path
            self.timeout: int = self.joern_config.timeout if self.joern_config.timeout else timeout
            self.server_endpoint: str = self.joern_config.server_endpoint if self.joern_config.server_endpoint else server_endpoint
        except Exception as e:
            self.logger.warning(f"配置加载失败，使用默认参数: {e}")
            # 使用传入的参数作为默认值
            self.joern_path: str = joern_path
            self.timeout: int = timeout
            self.server_endpoint: str = server_endpoint
            
        self._connected: bool = False
        self._server_process = None
        self._server_started_by_us: bool = False
        self._command_history = []  # 存储命令历史
        self._last_activity = time.time()
        self._client = None  # 初始化客户端为None
        self._consecutive_timeouts = 0  # 连续超时计数
        self._max_consecutive_timeouts = 3  # 最大连续超时次数
        
        self.logger.info(f"初始化JoernBridge: joern_path={self.joern_path}, timeout={self.timeout}, server_endpoint={self.server_endpoint}")
        
        # 自动启动Joern服务器
        self._setup_and_start_server()
        self._init_joern_server()
 
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
                            self.logger.warning(f"无法终止进程 {pid}: {e}")
            else:
                self.logger.info(f"未找到占用端口 {port} 的进程")
                
        except subprocess.TimeoutExpired:
            self.logger.warning("查找端口占用进程超时")
        except FileNotFoundError:
            # lsof命令不存在，尝试使用netstat + ps
            try:
                self._kill_process_on_port_fallback(port)
            except Exception as e:
                self.logger.warning(f"无法终止端口 {port} 的占用进程: {e}")
        except Exception as e:
            self.logger.warning(f"终止端口占用进程时出错: {e}")

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
                                        self.logger.warning(f"无法终止进程 {pid}: {e}")
        except Exception as e:
            self.logger.warning(f"备用终止方法失败: {e}")

    def _setup_java_environment(self) -> None:
        """设置Java环境变量，增加栈空间和内存"""
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

    def _setup_and_start_server(self) -> None:
        """强制启动新的Joern服务器，不考虑端口占用"""
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
            self.logger.error(f"设置和启动服务器失败: {e}")
            raise RuntimeError(f"无法启动Joern服务器: {e}")


    def _start_joern_server(self) -> bool:
        """启动joern server，包含增强的JVM参数"""
        try:
            # 解析server endpoint
            host, port_str = self.server_endpoint.split(':')
            port = int(port_str)
        
            # 构建启动命令
            joern_cmd = [
                self.joern_path,
                "--server",
            ]
            
            # 设置JVM环境变量，包含栈空间和内存优化
            env = os.environ.copy()
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
            
            current_java_opts = env.get('JAVA_OPTS', '')
            new_java_opts = ' '.join(java_opts)
            env['JAVA_OPTS'] = f"{current_java_opts} {new_java_opts}".strip()
            env['_JAVA_OPTIONS'] = new_java_opts
            
            self.logger.info(f"启动joern server: {' '.join(joern_cmd)}")
            self.logger.info(f"JVM参数: {new_java_opts}")
            
            # 启动进程
            self._server_process = subprocess.Popen(
                joern_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                env=env  # 传递包含JVM参数的环境变量
            )
            
            # 输出进程PID
            self.logger.info(f"joern server进程已启动，PID: {self._server_process.pid}")
            
            # 等待服务器启动
            max_wait_time = 45  # 增加等待时间，因为有更多JVM参数
            start_time = time.time()
            
            while time.time() - start_time < max_wait_time:
                if self._server_process.poll() is not None:
                    # 进程已退出
                    stdout, stderr = self._server_process.communicate()
                    self.logger.error(f"joern server启动失败，退出码: {self._server_process.returncode}")
                    self.logger.error(f"stdout: {stdout}")
                    self.logger.error(f"stderr: {stderr}")
                    return False
                
                if self._is_port_open(host, port):
                    self.logger.info("joern server启动成功")
                    self._server_started_by_us = True
                    return True
                
                time.sleep(1)
            
            self.logger.error("joern server启动超时")
            if self._server_process:
                self._server_process.terminate()
            return False
            
        except Exception as e:
            self.logger.error(f"启动joern server失败: {e}")
            return False

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
        关闭与Joern服务器的连接，如果server是我们启动的则关闭它
        """
        try:
            if self._client:
                self.logger.info("关闭Joern服务器连接")
                self._client = None
                self._connected = False
            
            # 如果server是我们启动的，则关闭它
            if self._server_started_by_us and self._server_process:
                self.logger.info("关闭我们启动的joern server")
                self._server_process.terminate()
                try:
                    self._server_process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    self.logger.warning("joern server未正常退出，强制终止")
                    self._server_process.kill()
                    self._server_process.wait()
                self._server_process = None
                self._server_started_by_us = False
                
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
        发送命令到Joern服务器并返回输出，支持超时重传
        
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
        
        # 使用传入的超时时间或默认超时时间，但为复杂查询增加更长的超时
        base_timeout = timeout if timeout is not None else self.timeout
        
        # 根据命令类型动态调整超时时间
        if any(keyword in cmd.lower() for keyword in ['method', 'call', 'dataflow', 'sink', 'source']):
            effective_timeout = max(base_timeout, 60)  # 复杂查询至少60秒
            self.logger.debug(f"检测到复杂查询，超时时间调整为: {effective_timeout}秒")
        else:
            effective_timeout = base_timeout
        
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
        
        # 重试机制配置
        max_retries = 2  # 减少重试次数，因为超时重试通常没有用
        retry_delay = 3  # 增加重试间隔时间
        
        for attempt in range(max_retries):
            start_time = time.time()
            try:
                # 确保连接可用
                self._ensure_connection()
                
                if not self._client:
                    raise RuntimeError("无法建立或维持Joern服务器连接")
                
                self.logger.debug(f"执行命令 (尝试 {attempt + 1}/{max_retries}, 超时:{effective_timeout}s): {cmd}")
                
                # 使用超时执行命令
                response = self._execute_with_timeout(cmd, effective_timeout)
                duration = time.time() - start_time
                
                if response is not None:
                    self._last_activity = time.time()
                    # 成功执行，重置连续超时计数
                    self._consecutive_timeouts = 0
                    # 解析响应
                    output = self._parse_server_response(response)
                    self.logger.debug(f"命令执行成功，耗时: {duration:.2f}秒")
                    return output
                else:
                    self.logger.warning(f"命令执行返回空结果，尝试 {attempt + 1}/{max_retries}")
                    
            except Exception as e:
                duration = time.time() - start_time
                error_msg = str(e)
                is_timeout = "timeout" in error_msg.lower() or "超时" in error_msg or "TimeoutError" in error_msg
                
                if is_timeout:
                    self._consecutive_timeouts += 1
                    self.logger.warning(f"命令执行超时 (尝试 {attempt + 1}/{max_retries}，连续超时: {self._consecutive_timeouts}次，耗时: {duration:.2f}秒): {cmd}")
                    
                    # 检查是否达到最大连续超时次数
                    if self._consecutive_timeouts >= self._max_consecutive_timeouts:
                        self.logger.error(f"连续超时达到 {self._max_consecutive_timeouts} 次，可能Joern服务器已崩溃")
                        # 抛出特殊异常，让上层处理
                        raise RuntimeError(f"JOERN_SERVER_CRASHED: 连续超时{self._consecutive_timeouts}次，服务器可能已崩溃")
                    
                    # 对于超时错误，如果是第一次，尝试发送简单命令测试连接
                    if attempt == 0:
                        try:
                            test_response = self._execute_with_timeout("1+1", 5)
                            if test_response:
                                self.logger.info("连接正常，可能是查询过于复杂，增加超时时间")
                                effective_timeout = min(effective_timeout * 2, 300)  # 最多5分钟
                            else:
                                self.logger.warning("连接测试失败，可能需要重连")
                        except:
                            self.logger.warning("连接测试异常，准备重连")
                else:
                    # 非超时错误，重置连续超时计数
                    self._consecutive_timeouts = 0
                    self.logger.warning(f"命令执行失败 (尝试 {attempt + 1}/{max_retries}): {error_msg}")
                
                # 如果不是最后一次尝试，等待后重试
                if attempt < max_retries - 1:
                    self.logger.info(f"等待 {retry_delay} 秒后重试...")
                    time.sleep(retry_delay)
                    
                    # 连接问题时尝试重新连接
                    if is_timeout or "连接" in error_msg:
                        try:
                            self._reconnect()
                        except Exception as reconnect_err:
                            self.logger.error(f"重连失败: {reconnect_err}")
                else:
                    # 最后一次尝试也失败了
                    if is_timeout:
                        self.logger.error(f"命令持续超时，可能是服务器性能问题或查询过于复杂: {cmd}")
                        raise RuntimeError(f"命令执行超时 (已重试{max_retries}次，最后超时时间:{effective_timeout}s): {cmd}")
                    else:
                        raise RuntimeError(f"命令执行失败 (已重试{max_retries}次): {error_msg}")
        
        return None

    def _execute_with_timeout(self, cmd: str, timeout: int) -> Dict[str, Any] | None:
        """
        使用超时机制执行命令
        
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
        import signal
        
        def execute_command():
            try:
                if not self._client:
                    raise RuntimeError("客户端连接未初始化")
                
                # 添加进度日志
                self.logger.debug(f"开始执行命令: {cmd[:100]}...")
                start_time = time.time()
                
                result = self._client.execute(cmd)
                
                duration = time.time() - start_time
                self.logger.debug(f"命令执行完成，耗时: {duration:.2f}秒")
                
                return result
            except Exception as e:
                self.logger.error(f"执行命令时出错: {e}")
                raise
        
        # 使用线程池执行命令
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(execute_command)
            try:
                # 添加进度监控
                check_interval = min(10, timeout // 4)  # 每隔1/4超时时间检查一次
                elapsed = 0
                
                while elapsed < timeout:
                    try:
                        result = future.result(timeout=check_interval)
                        return result
                    except concurrent.futures.TimeoutError:
                        elapsed += check_interval
                        if elapsed < timeout:
                            self.logger.debug(f"命令执行中... 已耗时: {elapsed}秒 / {timeout}秒")
                        continue
                
                # 超时了
                self.logger.error(f"命令执行超时 ({timeout}秒): {cmd}")
                future.cancel()
                raise TimeoutError(f"命令执行超时: {cmd}")
                
            except concurrent.futures.TimeoutError:
                self.logger.error(f"命令执行超时 ({timeout}秒): {cmd}")
                future.cancel()
                raise TimeoutError(f"命令执行超时: {cmd}")
            except Exception as e:
                self.logger.error(f"命令执行异常: {e}")
                raise RuntimeError(f"命令执行失败: {e}")

    def _reconnect(self) -> None:
        """
        重新建立与Joern服务器的连接
        """
        try:
            self.logger.info("尝试重新连接到Joern服务器...")
            
            # 关闭现有连接
            if self._client:
                try:
                    self._client = None
                except:
                    pass
            
            self._connected = False
            
            # 等待一段时间再重连
            time.sleep(2)
            
            # 检查服务器是否还在运行
            host, port_str = self.server_endpoint.split(':')
            port = int(port_str)
            
            if not self._is_port_open(host, port):
                self.logger.warning("Joern服务器端口不可达，尝试重启服务器...")
                if self._server_started_by_us and self._server_process:
                    # 如果是我们启动的服务器，重启它
                    self._restart_server()
                else:
                    raise RuntimeError("Joern服务器不可达且非本程序启动")
            
            # 重新初始化连接
            self._init_joern_server()
            
        except Exception as e:
            self.logger.error(f"重连失败: {e}")
            raise RuntimeError(f"无法重新连接到Joern服务器: {e}")

    def force_restart_server(self) -> bool:
        """
        强制重启Joern服务器（用于服务器崩溃后的恢复）
        """
        try:
            self.logger.warning("强制重启Joern服务器...")
            
            # 重置连续超时计数
            self._consecutive_timeouts = 0
            
            # 关闭现有连接
            if self._client:
                self._client = None
            self._connected = False
            
            # 如果是我们启动的服务器，强制终止它
            if self._server_started_by_us and self._server_process:
                self.logger.info("强制终止当前Joern服务器进程...")
                try:
                    self._server_process.kill()
                    self._server_process.wait(timeout=5)
                except:
                    pass
                self._server_process = None
                self._server_started_by_us = False
            
            # 解析端口并强制清理
            host, port_str = self.server_endpoint.split(':')
            port = int(port_str)
            
            # 强制终止占用端口的进程
            self._kill_process_on_port(port)
            
            # 等待端口释放
            time.sleep(5)
            
            # 重新设置Java环境和启动服务器
            self._setup_java_environment()
            
            # 启动新服务器
            if not self._start_joern_server():
                self.logger.error("强制重启Joern服务器失败")
                return False
            
            # 重新建立连接
            self._init_joern_server()
            
            self.logger.info("Joern服务器强制重启成功")
            return True
            
        except Exception as e:
            self.logger.error(f"强制重启服务器失败: {e}")
            return False

    def _restart_server(self) -> None:
        """
        重启Joern服务器（仅当服务器是由本程序启动时）
        """
        if not self._server_started_by_us or not self._server_process:
            raise RuntimeError("无法重启非本程序启动的服务器")
        
        try:
            self.logger.info("正在重启Joern服务器...")
            
            # 关闭现有服务器
            self._server_process.terminate()
            try:
                self._server_process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.logger.warning("服务器未正常退出，强制终止")
                self._server_process.kill()
                self._server_process.wait()
            
            # 等待端口释放
            time.sleep(3)
            
            # 重新启动服务器
            if not self._start_joern_server():
                raise RuntimeError("重启Joern服务器失败")
                
        except Exception as e:
            self.logger.error(f"重启服务器失败: {e}")
            raise

    def health_check(self) -> bool:
        """
        健康检查：验证Joern服务器是否正常工作
        
        Returns:
            True if healthy, False otherwise
        """
        try:
            # 发送简单的测试命令
            result = self.send_command("1 + 1", timeout=10)
            if result is not None and isinstance(result, str):
                return "2" in result and not result.strip() == "=~"
            return False
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

    def __enter__(self):
        """上下文管理器进入"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器退出"""
        self.close_shell()
