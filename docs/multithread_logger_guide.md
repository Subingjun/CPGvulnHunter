# 多线程Logger使用指南

## 概述

这个多线程logger框架专为CPGvulnHunter项目设计，支持每个线程使用独立的日志文件，避免文件锁竞争，提供优秀的性能和线程安全性。

## 核心特性

1. **线程隔离**: 每个线程拥有独立的logger实例和文件handler
2. **无锁设计**: 避免线程间的同步开销，提高性能
3. **自动清理**: 支持线程结束后自动清理资源
4. **向后兼容**: 保持与现有ThreadLogger接口的兼容性

## 使用方式

### 1. 基本使用（推荐）

```python
from CPGvulnHunter.utils.logger_config import LoggerConfigurator

# 为当前线程设置独立的logger
logger = LoggerConfigurator.setup_thread_logger(
    thread_name="TaskProcessor",
    log_file="logs/task_processor.log",
    level="INFO",
    console=True
)

logger.info("开始处理任务")
logger.warning("这是一个警告")
logger.error("这是一个错误")

# 任务结束后清理
LoggerConfigurator.cleanup_thread_loggers()
```

### 2. 兼容现有代码

```python
from CPGvulnHunter.utils.logger_config import ThreadLogger

# 与现有ThreadLogger接口完全兼容
logger = ThreadLogger.setup(
    name="TaskProcessor",
    level="INFO",
    log_file="logs/task_processor.log",
    console=True
)

logger.info("处理中...")

# 清理
ThreadLogger.cleanup()
```

### 3. 在Task类中的使用

```python
class Task:
    def __init__(self, target_src_path: str, output_path: Path):
        # 为每个任务创建独立的日志文件
        thread_name = f"task_{Path(target_src_path).name}"
        log_file = str(output_path / "task.log")
        
        self.logger = LoggerConfigurator.setup_thread_logger(
            thread_name=thread_name,
            log_file=log_file,
            level="INFO",
            console=True
        )
        
    def run(self):
        self.logger.info("任务开始")
        try:
            # 任务执行逻辑
            pass
        finally:
            # 清理logger
            LoggerConfigurator.cleanup_thread_loggers()
```

### 4. 线程池中的使用

```python
from concurrent.futures import ThreadPoolExecutor

def worker_function(task_id: int):
    # 每个worker线程独立的logger
    logger = LoggerConfigurator.setup_thread_logger(
        thread_name=f"Worker-{task_id}",
        log_file=f"logs/worker_{task_id}.log",
        level="INFO"
    )
    
    try:
        logger.info(f"Worker {task_id} 开始工作")
        # 工作逻辑
        logger.info(f"Worker {task_id} 完成工作")
    finally:
        LoggerConfigurator.cleanup_thread_loggers()

# 使用线程池
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(worker_function, i) for i in range(10)]
    for future in futures:
        future.result()
```

## 配置选项

### LoggerConfigurator.setup_thread_logger 参数

- `thread_name`: 线程名称，用于日志标识（可选）
- `log_file`: 日志文件路径（可选，不设置则不记录文件）
- `level`: 日志级别（"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"）
- `console`: 是否同时输出到控制台（默认True）

### 日志格式

- 控制台格式: `%(asctime)s - {thread_name} - %(levelname)s - %(message)s`
- 文件格式: 相同

## 最佳实践

### 1. 文件命名规范

```python
# 按任务类型命名
log_file = f"logs/{task_type}_{task_id}.log"

# 按时间戳命名
import datetime
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = f"logs/task_{timestamp}_{thread_id}.log"

# 按源码路径命名
src_name = Path(source_path).stem
log_file = f"logs/analysis_{src_name}.log"
```

### 2. 资源清理

```python
def task_function():
    logger = LoggerConfigurator.setup_thread_logger(...)
    try:
        # 任务逻辑
        pass
    finally:
        # 必须清理，防止资源泄露
        LoggerConfigurator.cleanup_thread_loggers()
```

### 3. 异常处理

```python
def safe_task_function():
    logger = None
    try:
        logger = LoggerConfigurator.setup_thread_logger(...)
        logger.info("任务开始")
        # 可能抛出异常的代码
        risky_operation()
        logger.info("任务完成")
    except Exception as e:
        if logger:
            logger.error(f"任务失败: {e}")
        raise
    finally:
        if logger:
            LoggerConfigurator.cleanup_thread_loggers()
```

## 性能优化

1. **避免共享文件**: 每个线程使用不同的日志文件，避免文件锁竞争
2. **合理设置缓冲**: Python的logging模块内置缓冲机制
3. **及时清理**: 任务完成后及时调用cleanup方法

## 故障排除

### 常见问题

1. **日志文件无法创建**
   - 检查目录权限
   - 确保父目录存在

2. **日志重复输出**
   - 检查是否多次调用setup方法
   - 确保在finally块中调用cleanup

3. **线程间日志混乱**
   - 确保每个线程使用不同的log_file路径
   - 检查thread_name是否唯一

### 调试技巧

```python
# 启用调试模式
logger = LoggerConfigurator.setup_thread_logger(
    thread_name="DebugTask",
    log_file="logs/debug.log",
    level="DEBUG",  # 设置为DEBUG级别
    console=True
)

# 输出线程信息
import threading
logger.debug(f"当前线程ID: {threading.get_ident()}")
logger.debug(f"当前线程名: {threading.current_thread().name}")
```

## 与现有系统集成

这个logger框架完全兼容您现有的代码结构，可以直接替换原有的ThreadLogger使用，无需修改业务逻辑代码。

主要改进：
- 更好的线程安全性
- 更清晰的资源管理
- 更灵活的配置选项
- 更完善的错误处理
