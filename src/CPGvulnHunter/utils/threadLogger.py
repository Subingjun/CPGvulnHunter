import threading
import logging
import time
from pathlib import Path
from typing import Dict, Optional, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ThreadLoggerConfig:
    """线程Logger配置"""
    thread_name: str
    log_file: Optional[str] = None
    level: str = "DEBUG"
    console: bool = True
    format_string: Optional[str] = None
    file_mode: str = "a"
    encoding: str = "utf-8"
    max_file_size: Optional[int] = None  # 字节
    backup_count: int = 3

class LoggerManager:
    """线程敏感的Logger管理器"""
    
    def __init__(self):
        self._local = threading.local()
        self._global_lock = threading.Lock()
        self._thread_configs: Dict[int, ThreadLoggerConfig] = {}
        self._thread_loggers: Dict[int, logging.Logger] = {}
        self._default_config = ThreadLoggerConfig(
            thread_name="DefaultThread",
            level="INFO",
            console=True
        )
    
    def setup_thread_logger(self, config: ThreadLoggerConfig) -> logging.Logger:
        """为当前线程设置独立的logger"""
        thread_id = threading.get_ident()
        thread_name = threading.current_thread().name
        
        # 使用提供的线程名或当前线程名
        if not config.thread_name or config.thread_name == "DefaultThread":
            config.thread_name = thread_name
        
        # 生成唯一的logger名称
        logger_name = f"{config.thread_name}_{thread_id}"
        
        # 创建logger
        logger = logging.getLogger(logger_name)
        
        # 清除现有处理器
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)
        
        # 设置日志级别
        log_level = getattr(logging, config.level.upper(), logging.INFO)
        logger.setLevel(log_level)
        
        # 创建格式化器

        formatter = logging.Formatter(
            f'%(asctime)s - {config.thread_name} - %(levelname)s - %(message)s'
        )       
        
        # 控制台处理器
        if config.console:
            console_handler = logging.StreamHandler()
            console_handler.setLevel("INFO")
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
        
        # 文件处理器
        if config.log_file:
            try:
                log_path = Path(config.log_file)
                log_path.parent.mkdir(parents=True, exist_ok=True)
                #单个thread的日志不需要采用轮转
                file_handler = logging.FileHandler(
                    config.log_file,
                    mode=config.file_mode,
                    encoding=config.encoding
                )
                
                file_handler.setLevel("DEBUG")
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
                
                # 存储文件处理器引用
                if not hasattr(self._local, 'file_handlers'):
                    self._local.file_handlers = []
                self._local.file_handlers.append(file_handler)
                
            except Exception as e:
                logger.error(f"无法创建文件处理器: {e}", exc_info=True)
        
        # 防止日志传播到根logger
        logger.propagate = False
        
        # 存储配置和logger
        with self._global_lock:
            self._thread_configs[thread_id] = config
            self._thread_loggers[thread_id] = logger
        
        # 在线程本地存储中保存logger
        self._local.logger = logger
        self._local.config = config
        
        logger.info(f"线程 {config.thread_name} ({thread_id}) Logger初始化完成")
        return logger
    
    def get_thread_logger(self) -> logging.Logger:
        """获取当前线程的logger"""
        if hasattr(self._local, 'logger'):
            return self._local.logger
        
        # 如果没有设置，使用默认配置
        thread_id = threading.get_ident()
        thread_name = threading.current_thread().name
        
        default_config = ThreadLoggerConfig(
            thread_name=thread_name,
            level="DEBUG",
            console=True
        )
        
        return self.setup_thread_logger(default_config)
    
    def update_thread_logger_level(self, level: str):
        """更新当前线程logger的日志级别"""
        if hasattr(self._local, 'logger'):
            log_level = getattr(logging, level.upper(), logging.INFO)
            self._local.logger.setLevel(log_level)
            
            # 更新所有处理器的级别
            for handler in self._local.logger.handlers:
                handler.setLevel(log_level)
            
            self._local.logger.info(f"日志级别已更新为: {level}")
    
    def add_file_handler(self, log_file: str, level: str = "INFO", 
                        format_string: Optional[str] = None):
        """为当前线程的logger添加文件处理器"""
        if not hasattr(self._local, 'logger'):
            self.get_thread_logger()
        
        try:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            
            log_level = getattr(logging, level.upper(), logging.INFO)
            file_handler.setLevel(log_level)
            
            if format_string:
                formatter = logging.Formatter(format_string)
            else:
                thread_name = getattr(self._local, 'config', self._default_config).thread_name
                formatter = logging.Formatter(
                    f'%(asctime)s - {thread_name} - %(levelname)s - %(message)s'
                )
            
            file_handler.setFormatter(formatter)
            self._local.logger.addHandler(file_handler)
            
            # 存储处理器引用
            if not hasattr(self._local, 'file_handlers'):
                self._local.file_handlers = []
            self._local.file_handlers.append(file_handler)
            
            self._local.logger.info(f"添加文件处理器: {log_file}")
            
        except Exception as e:
            if hasattr(self._local, 'logger'):
                self._local.logger.error(f"添加文件处理器失败: {e}", exc_info=True)
    
    def cleanup_thread_logger(self):
        """清理当前线程的logger和处理器"""
        thread_id = threading.get_ident()
        
        # 清理线程本地的处理器
        if hasattr(self._local, 'file_handlers'):
            for handler in self._local.file_handlers:
                try:
                    handler.close()
                except Exception as e:
                    # 在清理阶段，避免使用可能已损坏的logger
                    print(f"清理文件处理器时出错: {e}")
            self._local.file_handlers.clear()
        
        # 清理logger处理器
        if hasattr(self._local, 'logger'):
            for handler in self._local.logger.handlers[:]:
                try:
                    handler.close()
                    self._local.logger.removeHandler(handler)
                except Exception as e:
                    # 在清理阶段，避免使用可能已损坏的logger
                    print(f"清理logger处理器时出错: {e}")
        
        # 从全局存储中移除
        with self._global_lock:
            self._thread_configs.pop(thread_id, None)
            self._thread_loggers.pop(thread_id, None)
        
        # 清理线程本地存储
        if hasattr(self._local, 'logger'):
            delattr(self._local, 'logger')
        if hasattr(self._local, 'config'):
            delattr(self._local, 'config')
        if hasattr(self._local, 'file_handlers'):
            delattr(self._local, 'file_handlers')
    
    def get_all_thread_loggers(self) -> Dict[int, logging.Logger]:
        """获取所有线程的logger"""
        with self._global_lock:
            return self._thread_loggers.copy()
    
    def get_thread_logger_status(self) -> Dict[str, Any]:
        """获取当前线程logger状态"""
        thread_id = threading.get_ident()
        thread_name = threading.current_thread().name
        
        status = {
            "thread_id": thread_id,
            "thread_name": thread_name,
            "has_logger": hasattr(self._local, 'logger'),
            "handlers": []
        }
        
        if hasattr(self._local, 'logger'):
            logger = self._local.logger
            status.update({
                "logger_name": logger.name,
                "logger_level": logging.getLevelName(logger.level),
                "handler_count": len(logger.handlers)
            })
            
            for i, handler in enumerate(logger.handlers):
                handler_info = {
                    "index": i,
                    "type": type(handler).__name__,
                    "level": logging.getLevelName(handler.level)
                }
                
                if hasattr(handler, 'baseFilename'):
                    handler_info["file"] = handler.baseFilename
                
                status["handlers"].append(handler_info)
        
        return status

# 全局实例
_thread_logger_manager = LoggerManager()

# 便捷函数
def setup_thread_logger(thread_name: str = None, 
                       log_file: str = None,
                       console: bool = True,
                       format_string: str = None,
                       max_file_size: int = None,
                       backup_count: int = 3) -> logging.Logger:
    """设置当前线程的logger"""
    config = ThreadLoggerConfig(
        thread_name=thread_name or threading.current_thread().name,
        log_file=log_file,
        level="DEBUG",
        console=console,
        format_string=format_string,
        max_file_size=max_file_size,
        backup_count=backup_count
    )
    return _thread_logger_manager.setup_thread_logger(config)

def get_thread_logger() -> logging.Logger:
    """获取当前线程的logger"""
    return _thread_logger_manager.get_thread_logger()

def cleanup_thread_logger():
    """清理当前线程的logger"""
    _thread_logger_manager.cleanup_thread_logger()

def get_thread_logger_status() -> Dict[str, Any]:
    """获取当前线程logger状态"""
    return _thread_logger_manager.get_thread_logger_status()

# 上下文管理器
class ThreadLoggerContext:
    """线程Logger上下文管理器"""
    
    def __init__(self, **kwargs):
        self.config_kwargs = kwargs
        self.logger = None
    
    def __enter__(self) -> logging.Logger:
        self.logger = setup_thread_logger(**self.config_kwargs)
        return self.logger
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        cleanup_thread_logger()

# 装饰器
def with_thread_logger(**logger_kwargs):
    """线程Logger装饰器"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            with ThreadLoggerContext(**logger_kwargs) as logger:
                # 将logger作为第一个参数传递给函数
                return func(logger, *args, **kwargs)
        return wrapper
    return decorator

if __name__ == "__main__":
    # 测试代码
    import concurrent.futures
    import time
    
    def test_thread_function(thread_id: int):
        """测试线程函数"""
        # 设置线程专用logger
        logger = setup_thread_logger(
            thread_name=f"TestThread-{thread_id}",
            log_file=f"logs/thread_{thread_id}.log",
            level="DEBUG",
            console=True,
            max_file_size=1024*1024,  # 1MB
            backup_count=3
        )
        
        try:
            logger.info(f"线程 {thread_id} 开始执行")
            
            for i in range(5):
                logger.debug(f"线程 {thread_id} - 循环 {i+1}")
                time.sleep(0.5)
            
            logger.warning(f"线程 {thread_id} - 这是一个警告")
            logger.error(f"线程 {thread_id} - 这是一个错误", exc_info=True)
            
            # 获取状态
            status = get_thread_logger_status()
            logger.info(f"Logger状态: {status}")
            
            logger.info(f"线程 {thread_id} 执行完成")
            
        finally:
            # 清理资源
            cleanup_thread_logger()
    
    def test_context_manager():
        """测试上下文管理器"""
        with ThreadLoggerContext(
            thread_name="ContextThread",
            log_file="logs/context_test.log",
            level="INFO"
        ) as logger:
            logger.info("使用上下文管理器的logger")
            logger.warning("这是一个测试")
    
    @with_thread_logger(
        thread_name="DecoratorThread",
        log_file="logs/decorator_test.log",
        level="DEBUG"
    )
    def test_decorator(logger: logging.Logger):
        """测试装饰器"""
        logger.info("使用装饰器的logger")
        logger.debug("这是调试信息")
    
    # 运行测试
    print("开始测试线程敏感Logger...")
    
    # 多线程测试
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(test_thread_function, i) for i in range(3)]
        concurrent.futures.wait(futures)
    
    # 上下文管理器测试
    test_context_manager()
    
    # 装饰器测试
    test_decorator()
    
    print("测试完成！")