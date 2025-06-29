"""
日志配置器模块

提供统一的日志配置功能，独立于数据类，支持多线程环境
每个线程可以拥有独立的logger实例
"""
import logging
import logging.handlers
from pathlib import Path
from typing import Optional, Dict, Any, Union
import inspect
import threading
import queue
import time
import os
from concurrent.futures import ThreadPoolExecutor

from CPGvulnHunter.core.config import LoggingConfig


class ThreadSafeQueueHandler(logging.Handler):
    """线程安全的队列处理器，用于多线程环境下的日志处理"""
    
    def __init__(self, queue: queue.Queue):
        super().__init__()
        self.queue = queue
    
    def emit(self, record):
        try:
            self.queue.put_nowait(record)
        except queue.Full:
            pass  # 队列满时丢弃日志记录


class ThreadLocalLoggerManager:
    """线程本地日志管理器 - 每个线程独立文件handler版本"""
    
    def __init__(self):
        self._local = threading.local()
        self._global_config = None
        self._lock = threading.Lock()  # 只用于保护全局配置
    
    def set_global_config(self, config: LoggingConfig):
        """设置全局配置"""
        with self._lock:
            self._global_config = config
    
    def get_thread_logger(self, name: str = None) -> logging.Logger:
        """获取当前线程的logger实例"""
        if not hasattr(self._local, 'logger_cache'):
            self._local.logger_cache = {}
        
        # 如果没有指定名称，自动获取调用者模块名
        if name is None:
            frame = inspect.currentframe()
            try:
                caller_frame = frame.f_back
                name = caller_frame.f_globals.get('__name__', 'unknown')
            finally:
                del frame
        
        # 生成线程特定的logger名称
        thread_id = threading.get_ident()
        thread_logger_name = f"{name}.thread_{thread_id}"
        
        # 检查缓存
        if thread_logger_name in self._local.logger_cache:
            return self._local.logger_cache[thread_logger_name]
        
        # 创建新的线程logger（使用全局配置）
        logger = self._create_thread_logger(thread_logger_name)
        self._local.logger_cache[thread_logger_name] = logger
        
        return logger
    
    def _create_thread_logger(self, logger_name: str) -> logging.Logger:
        """创建线程特定的logger（使用全局配置的控制台输出）"""
        logger = logging.getLogger(logger_name)
        
        # 防止重复配置
        if logger.handlers:
            return logger
        
        # 设置日志级别
        if self._global_config:
            level = getattr(logging, self._global_config.level.upper(), logging.INFO)
            logger.setLevel(level)
        else:
            logger.setLevel(logging.INFO)
        
        # 添加线程ID到格式化器
        thread_id = threading.get_ident()
        formatter = logging.Formatter(
            f'%(asctime)s - %(name)s - [Thread-{thread_id}] - %(levelname)s - %(message)s'
        )
        
        # 控制台处理器（每个线程独立）
        if self._global_config and self._global_config.console:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logger.level)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
        
        # 防止向根logger传播
        logger.propagate = False
        
        return logger
    
    def setup_thread_logger(self, thread_name: str = None, 
                           log_file: str = None,
                           level: str = "INFO",
                           console: bool = True) -> logging.Logger:
        """为当前线程设置独立的logger配置"""
        thread_id = threading.get_ident()
        
        if thread_name is None:
            thread_name = f"Thread-{thread_id}"
        
        # 每个线程都有唯一的logger名称
        logger_name = f"{thread_name}.{thread_id}"
        logger = logging.getLogger(logger_name)
        
        # 清除现有处理器（避免重复设置）
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)
        
        # 设置级别
        log_level = getattr(logging, level.upper(), logging.INFO)
        logger.setLevel(log_level)
        
        # 创建格式化器
        formatter = logging.Formatter(
            f'%(asctime)s - {thread_name} - %(levelname)s - %(message)s'
        )
        
        # 控制台处理器
        if console:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(log_level)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
        
        # 文件处理器（每个线程独立文件）
        if log_file:
            try:
                log_path = Path(log_file)
                log_path.parent.mkdir(parents=True, exist_ok=True)
                
                # 每个线程独立的文件handler，无需线程同步
                file_handler = logging.FileHandler(log_file, encoding='utf-8')
                file_handler.setLevel(log_level)
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
                
                # 存储handler引用便于清理
                if not hasattr(self._local, 'handlers'):
                    self._local.handlers = []
                self._local.handlers.append(file_handler)
                
            except Exception as e:
                print(f"警告：设置文件处理器失败: {e}")
        
        logger.propagate = False
        return logger
    
    def cleanup_thread_loggers(self):
        """清理当前线程的logger缓存和handlers"""
        if hasattr(self._local, 'logger_cache'):
            for logger in self._local.logger_cache.values():
                for handler in logger.handlers[:]:
                    handler.close()
                    logger.removeHandler(handler)
            self._local.logger_cache.clear()
        
        # 清理线程本地的文件handlers
        if hasattr(self._local, 'handlers'):
            for handler in self._local.handlers:
                try:
                    handler.close()
                except:
                    pass
            self._local.handlers.clear()


# 全局线程本地日志管理器实例
_thread_logger_manager = ThreadLocalLoggerManager()


class LoggerConfigurator:
    """日志配置器类 - 负责根据配置设置整个应用程序的日志系统"""
    _initialized = False
    _current_level = logging.INFO
    _lock = threading.Lock()  # 线程锁，确保线程安全

    @staticmethod
    def setup_logging(logging_config: LoggingConfig) -> None:
        """根据配置设置日志系统"""
        if LoggerConfigurator._initialized:
            print("警告: 日志系统已经初始化")
            return

        with LoggerConfigurator._lock:  # 加锁
            level = getattr(logging, logging_config.level.upper(), logging.INFO)
            LoggerConfigurator._current_level = level

            # 配置全局线程日志管理器
            _thread_logger_manager.set_global_config(logging_config)

            # 配置根logger
            root_logger = logging.getLogger()
            root_logger.setLevel(level)

            # 清除现有处理器
            for handler in root_logger.handlers[:]:
                root_logger.removeHandler(handler)

            formatter = logging.Formatter(logging_config.format)

            # 控制台处理器
            if logging_config.console:
                console_handler = logging.StreamHandler()
                console_handler.setLevel(level)
                console_handler.setFormatter(formatter)
                root_logger.addHandler(console_handler)

            # 文件处理器
            if logging_config.file:
                LoggerConfigurator._setup_file_handler(
                    root_logger, logging_config.file, level,
                    formatter, logging_config.max_file_size,
                    logging_config.backup_count
                )

            # 配置第三方库
            LoggerConfigurator._configure_third_party_loggers()

            LoggerConfigurator._initialized = True
            print(f"日志系统初始化完成，级别: {logging_config.level}")
            print("多线程日志支持已启用")

    @staticmethod
    def set_global_log_level(level: str) -> None:
        """简单设置全局日志级别"""
        try:
            log_level = getattr(logging, level.upper())
        except AttributeError:
            print(f"警告: 未知日志级别 '{level}'，使用 INFO")
            log_level = logging.INFO

        LoggerConfigurator._current_level = log_level

        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)

        for handler in root_logger.handlers:
            handler.setLevel(log_level)

        print(f"全局日志级别已设置为: {level.upper()}")

    @staticmethod
    def get_thread_logger(name: str = None) -> logging.Logger:
        """获取当前线程的独立logger实例"""
        return _thread_logger_manager.get_thread_logger(name)
    
    @staticmethod
    def setup_thread_logger(thread_name: str = None, 
                           log_file: str = None,
                           level: str = "INFO",
                           console: bool = True) -> logging.Logger:
        """为当前线程设置独立的logger配置"""
        return _thread_logger_manager.setup_thread_logger(thread_name, log_file, level, console)
    
    @staticmethod
    def cleanup_thread_loggers():
        """清理当前线程的logger缓存"""
        _thread_logger_manager.cleanup_thread_loggers()

    @staticmethod
    def get_auto_logger() -> logging.Logger:
        """自动获取调用者模块的logger"""
        frame = inspect.currentframe()
        try:
            caller_frame = frame.f_back
            module_name = caller_frame.f_globals.get('__name__', 'unknown')
            return logging.getLogger(module_name)
        finally:
            del frame

    @staticmethod
    def _configure_third_party_loggers() -> None:
        """配置第三方库日志级别"""
        for logger_name in ['urllib3', 'requests', 'websockets', 'httpx']:
            logging.getLogger(logger_name).setLevel(logging.WARNING)

    @staticmethod
    def setup_custom_file_handler(log_file: str,
                                  level: str = "INFO",
                                  max_file_size: str = "10MB",
                                  backup_count: int = 5) -> None:
        """
        为根日志记录器设置自定义文件处理器

        Args:
            log_file: 日志文件路径
            level: 日志级别
            max_file_size: 最大文件大小
            backup_count: 备份文件数量
        """
        root_logger = logging.getLogger()

        # 移除现有的文件处理器，避免重复
        file_handlers = [h for h in root_logger.handlers if isinstance(h, logging.handlers.RotatingFileHandler)]
        for handler in file_handlers:
            root_logger.removeHandler(handler)
            handler.close()

        # 设置日志级别
        log_level = getattr(logging, level.upper(), logging.INFO)

        # 创建格式化器
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # 调用内部方法
        LoggerConfigurator._setup_file_handler(
            root_logger, log_file, log_level, formatter, max_file_size, backup_count
        )

        print(f"日志文件处理器已设置: {log_file}")

    @staticmethod
    def _setup_file_handler(root_logger: logging.Logger,
                            log_file: str,
                            level: int,
                            formatter: logging.Formatter,
                            max_file_size: str,
                            backup_count: int) -> None:
        """
        设置文件处理器

        Args:
            root_logger: 根日志记录器
            log_file: 日志文件路径
            level: 日志级别
            formatter: 格式化器
            max_file_size: 最大文件大小
            backup_count: 备份文件数量
        """
        try:
            # 确保日志目录存在
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)

            # 解析文件大小
            size_bytes = LoggerConfigurator._parse_file_size(max_file_size)

            # 创建轮转文件处理器
            file_handler = logging.handlers.RotatingFileHandler(
                filename=log_file,
                maxBytes=size_bytes,
                backupCount=backup_count,
                encoding='utf-8'
            )
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)

        except Exception as e:
            # 如果文件处理器设置失败，至少保证控制台输出
            print(f"警告：文件日志处理器设置失败: {e}")

    @staticmethod
    def _parse_file_size(size_str: str) -> int:
        """
        解析文件大小字符串

        Args:
            size_str: 大小字符串，如 "10MB", "1GB"

        Returns:
            int: 字节数
        """
        size_str = size_str.upper().strip()

        # 提取数字和单位
        import re
        match = re.match(r'(\d+(?:\.\d+)?)\s*([KMGT]?B?)', size_str)
        if not match:
            return 10 * 1024 * 1024  # 默认10MB

        number, unit = match.groups()
        number = float(number)

        # 转换单位
        multipliers = {
            'B': 1,
            'KB': 1024,
            'MB': 1024 * 1024,
            'GB': 1024 * 1024 * 1024,
            'TB': 1024 * 1024 * 1024 * 1024
        }

        if not unit:
            unit = 'B'
        elif unit == 'K':
            unit = 'KB'
        elif unit == 'M':
            unit = 'MB'
        elif unit == 'G':
            unit = 'GB'
        elif unit == 'T':
            unit = 'TB'

        return int(number * multipliers.get(unit, 1))

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """
        获取指定名称的日志记录器

        Args:
            name: 日志记录器名称

        Returns:
            logging.Logger: 日志记录器实例
        """
        return logging.getLogger(name)

    @staticmethod
    def get_class_logger(cls) -> logging.Logger:
        """
        为类获取日志记录器

        Args:
            cls: 类对象

        Returns:
            logging.Logger: 日志记录器实例
        """
        module_name = cls.__module__
        class_name = cls.__name__
        return logging.getLogger(f"{module_name}.{class_name}")


class ThreadLogger:
    """线程Logger兼容类 - 为了保持与现有代码的兼容性"""
    
    @staticmethod
    def setup(name: str = None,
              level: str = "INFO", 
              log_file: str = None,
              console: bool = True) -> logging.Logger:
        """
        设置线程logger的兼容方法
        
        Args:
            name: logger名称，如果为None则自动获取
            level: 日志级别
            log_file: 日志文件路径
            console: 是否输出到控制台
        
        Returns:
            logging.Logger: 配置好的logger实例
        """
        return LoggerConfigurator.setup_thread_logger(
            thread_name=name,
            log_file=log_file,
            level=level,
            console=console
        )
    
    @staticmethod
    def get_logger(name: str = None) -> logging.Logger:
        """
        获取线程logger的兼容方法
        
        Args:
            name: logger名称
            
        Returns:
            logging.Logger: logger实例
        """
        return LoggerConfigurator.get_thread_logger(name)
    
    @staticmethod
    def cleanup():
        """清理线程logger的兼容方法"""
        LoggerConfigurator.cleanup_thread_loggers()


# 为了保持向后兼容性的别名
ThreadLocalLogger = ThreadLogger
