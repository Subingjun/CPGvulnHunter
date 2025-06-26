from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import logging
import json
import yaml
import threading
from pathlib import Path

@dataclass
class LLMConfig:
    """LLM 配置数据类"""
    base_url: str = ""
    api_key: str = ""
    model: str = ""
    timeout: int = 30
    max_tokens: int = 4096
    temperature: float = 0.1
    cache_enabled: bool = True
    cache_file: str = ""

@dataclass
class JoernConfig:
    """Joern配置"""
    installation_path: str = None
    timeout: int = 300
    memory_limit: str = "8G"
    cpg_var: str = "cpg"
    workspace_path: str = "workspace"
    max_retries = 3
    server_endpoint: str = None
    command_save_path: str = ""

@dataclass
class EngineConfig:
    """Engine核心配置"""
    max_call_depth: int = 20
    timeout_per_pass: int = 300
    parallel_execution: bool = False
    max_functions: int = 1000
    output_dir: str = "output"
    save_intermediate_results: bool = True
    report_format: str = "json"
    enabled_passes: List[str] = field(default_factory=lambda: ["init"])
    pass_config: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    pass_registry: Dict[str, str] = field(default_factory=dict)
    max_retries = 3


@dataclass
class LoggingConfig:
    """日志配置"""
    level: str = "DEBUG"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file: Optional[str] = None
    console: bool = True
    max_file_size: str = "10MB"
    backup_count: int = 5


class ConfigManager:
    """配置管理器单例类 - 直接管理所有配置"""
    _instance = None
    _lock = threading.Lock()
    _default_config_path = Path(__file__).parent / "default_config.yaml"
    # 配置实例
    _llm_config: LLMConfig = None
    _joern_config: JoernConfig = None
    _engine_config: EngineConfig = None
    _logging_config: LoggingConfig = None
    
    # 全局配置
    _project_name: str = "CPGvulnHunter"
    _version: str = "1.0.0"
    _debug_mode: bool = False
    _initialized: bool = False
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def initialize(cls, config_file: str = None):
        """初始化配置"""
        with cls._lock:
            if not cls._initialized:
                if config_file:
                    cls._load_from_file(config_file)
                else:
                    cls._load_defaults()
                cls._initialized = True
                logging.info("配置管理器初始化完成")
    
    @classmethod
    def _load_defaults(cls):
        """加载默认配置"""
        cls._llm_config = LLMConfig()
        cls._joern_config = JoernConfig()
        cls._engine_config = EngineConfig()
        cls._logging_config = LoggingConfig()
        logging.info("使用默认配置初始化")
    
    @classmethod
    def _load_from_file(cls, config_file: str):
        """从文件加载配置"""
        config_path = Path(config_file)
        
        logging.info(f"开始加载配置文件: {config_file}")
        
        if not config_path.exists():
            logging.warning(f"配置文件不存在: {config_file}，使用默认配置")
            cls._load_defaults()
            return
        
        try:
            config_data = cls._load_config_file(config_path)
            logging.info(f"配置文件读取成功，包含 {len(config_data)} 个顶级配置项")
            logging.debug(f"配置项: {list(config_data.keys())}")
        except Exception as e:
            logging.error(f"配置文件读取失败: {e}")
            cls._load_defaults()
            return
        
        # 加载各个子配置
        cls._load_llm_config(config_data)
        cls._load_joern_config(config_data)
        cls._load_engine_config(config_data)
        cls._load_logging_config(config_data)
        cls._load_global_config(config_data)
        
        logging.info("所有配置加载完成")
    
    @classmethod
    def _load_llm_config(cls, config_data: Dict[str, Any]):
        """加载LLM配置"""
        if 'llm' in config_data:
            llm_data = config_data['llm']
            cls._llm_config = LLMConfig(**llm_data)
            logging.info(f"LLM配置加载成功 - 模型: {cls._llm_config.model}")
        elif 'llm_client' in config_data:  # 兼容旧格式
            logging.warning("检测到旧格式的llm_client配置，正在兼容处理...")
            llm_client_data = config_data['llm_client']
            cls._llm_config = LLMConfig(
                api_key=llm_client_data.get('api_key', ''),
                base_url=llm_client_data.get('base_url', ''),
                model=llm_client_data.get('model', 'qwen2.5:14b')
            )
            logging.info(f"旧格式LLM配置转换成功 - 模型: {cls._llm_config.model}")
        else:
            cls._llm_config = LLMConfig()
            logging.warning("未找到LLM配置，使用默认值")
    
    @classmethod
    def _load_joern_config(cls, config_data: Dict[str, Any]):
        """加载Joern配置"""
        if 'joern' in config_data:
            joern_data = config_data['joern']
            cls._joern_config = JoernConfig(**joern_data)
            logging.info(f"Joern配置加载成功 - 安装路径: {cls._joern_config.installation_path}")
        else:
            cls._joern_config = JoernConfig()
            logging.warning("未找到Joern配置，使用默认值")
    
    @classmethod
    def _load_engine_config(cls, config_data: Dict[str, Any]):
        """加载Engine配置"""
        if 'engine' in config_data:
            engine_data = config_data['engine']
            cls._engine_config = EngineConfig(
                max_call_depth=engine_data.get('max_call_depth', 20),
                timeout_per_pass=engine_data.get('timeout_per_pass', 300),
                parallel_execution=engine_data.get('parallel_execution', False),
                max_functions=engine_data.get('max_functions', 1000),
                output_dir=engine_data.get('output_dir', 'output'),
                save_intermediate_results=engine_data.get('save_intermediate_results', True),
                report_format=engine_data.get('report_format', 'json'),
                enabled_passes=engine_data.get('enabled_passes', ["init"]),
                pass_config=engine_data.get('pass_config', {}),
                pass_registry=engine_data.get('pass_registry', {})
            )
            logging.info(f"Engine配置加载成功 - 启用Pass: {cls._engine_config.enabled_passes}")
        else:
            cls._engine_config = EngineConfig()
            logging.warning("未找到Engine配置，使用默认值")
    
    @classmethod
    def _load_logging_config(cls, config_data: Dict[str, Any]):
        """加载日志配置"""
        if 'logging' in config_data:
            logging_data = config_data['logging']
            cls._logging_config = LoggingConfig(**logging_data)
            logging.info(f"日志配置加载成功 - 级别: {cls._logging_config.level}")
        else:
            cls._logging_config = LoggingConfig()
            logging.warning("未找到日志配置，使用默认值")
    

    
    @classmethod
    def _load_global_config(cls, config_data: Dict[str, Any]):
        """加载全局配置"""
        cls._project_name = config_data.get('project_name', 'CPGvulnHunter')
        cls._version = config_data.get('version', '1.0.0')
        cls._debug_mode = config_data.get('debug_mode', False)
        logging.info(f"全局配置加载完成 - 项目: {cls._project_name}, 版本: {cls._version}")
    
    @classmethod
    def _load_config_file(cls, config_path: Path) -> Dict[str, Any]:
        """加载配置文件"""
        suffix = config_path.suffix.lower()
        
        with open(config_path, 'r', encoding='utf-8') as f:
            if suffix in ['.json']:
                return json.load(f)
            elif suffix in ['.yaml', '.yml']:
                return yaml.safe_load(f)
            else:
                raise ValueError(f"不支持的配置文件格式: {suffix}")
    
    # 获取配置的方法
    @classmethod
    def get_llm_config(cls) -> LLMConfig:
        """获取LLM配置"""
        if not cls._initialized:
            cls.initialize()
        return cls._llm_config
    
    @classmethod
    def get_joern_config(cls) -> JoernConfig:
        """获取Joern配置"""
        if not cls._initialized:
            cls.initialize()
        return cls._joern_config
    
    @classmethod
    def get_engine_config(cls) -> EngineConfig:
        """获取Engine配置"""
        if not cls._initialized:
            cls.initialize()
        return cls._engine_config
    
    @classmethod
    def get_logging_config(cls) -> LoggingConfig:
        """获取日志配置"""
        if not cls._initialized:
            cls.initialize()
        return cls._logging_config
    

    
    # 全局配置获取方法
    @classmethod
    def get_project_name(cls) -> str:
        """获取项目名称"""
        if not cls._initialized:
            cls.initialize()
        return cls._project_name
    
    @classmethod
    def get_version(cls) -> str:
        """获取版本"""
        if not cls._initialized:
            cls.initialize()
        return cls._version
    
    @classmethod
    def get_debug_mode(cls) -> bool:
        """获取调试模式"""
        if not cls._initialized:
            cls.initialize()
        return cls._debug_mode
    
    @classmethod
    def is_initialized(cls) -> bool:
        """检查是否已初始化"""
        return cls._initialized
    
    @classmethod
    def get_config_summary(cls) -> Dict[str, Any]:
        """获取配置摘要"""
        if not cls._initialized:
            cls.initialize()
        
        return {
            'project_name': cls._project_name,
            'version': cls._version,
            'debug_mode': cls._debug_mode,
            'llm_model': cls._llm_config.model,
            'llm_base_url': cls._llm_config.base_url,
            'joern_path': cls._joern_config.installation_path,
            'enabled_passes': cls._engine_config.enabled_passes,
            'output_dir': cls._engine_config.output_dir,
            'log_level': cls._logging_config.level
        }
    
    @classmethod
    def validate(cls) -> List[str]:
        """验证配置"""
        if not cls._initialized:
            cls.initialize()
        
        errors = []
        
        # 验证Joern路径
        joern_path = Path(cls._joern_config.installation_path)
        if not joern_path.exists():
            errors.append(f"Joern安装路径不存在: {cls._joern_config.installation_path}")
        
        # 验证LLM配置
        if not cls._llm_config.api_key:
            errors.append("LLM API密钥未设置")
        if not cls._llm_config.base_url:
            errors.append("LLM基础URL未设置")
        if not cls._llm_config.model:
            errors.append("LLM模型未设置")
        
        # 验证输出目录
        output_path = Path(cls._engine_config.output_dir)
        try:
            output_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            errors.append(f"无法创建输出目录 {cls._engine_config.output_dir}: {e}")
        
        return errors
    
    @classmethod
    def reload_config(cls, config_file: str):
        """重新加载配置"""
        with cls._lock:
            cls._initialized = False
            cls._load_from_file(config_file)
            cls._initialized = True
            logging.info(f"配置已重新加载: {config_file}")
    
    @classmethod
    def reset(cls):
        """重置配置管理器（主要用于测试）"""
        with cls._lock:
            cls._instance = None
            cls._initialized = False
            cls._llm_config = None
            cls._joern_config = None
            cls._engine_config = None
            cls._logging_config = None
            cls._vulnerability_detection_config = None
    
    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """转换为字典格式"""
        if not cls._initialized:
            cls.initialize()
        
        return {
            'project_name': cls._project_name,
            'version': cls._version,
            'debug_mode': cls._debug_mode,
            'llm': {
                'api_key': cls._llm_config.api_key,
                'base_url': cls._llm_config.base_url,
                'model': cls._llm_config.model,
                'temperature': cls._llm_config.temperature,
                'max_tokens': cls._llm_config.max_tokens,
                'timeout': cls._llm_config.timeout,
                'cache_enabled': cls._llm_config.cache_enabled,
                'cache_file': cls._llm_config.cache_file
            },
            'joern': {
                'installation_path': cls._joern_config.installation_path,
                'timeout': cls._joern_config.timeout,
                'memory_limit': cls._joern_config.memory_limit,
                'cpg_var': cls._joern_config.cpg_var,
                'workspace_path': cls._joern_config.workspace_path,
                'enable_cache': cls._joern_config.enable_cache,
                'cache_dir': cls._joern_config.cache_dir
            },
            'engine': {
                'max_call_depth': cls._engine_config.max_call_depth,
                'timeout_per_pass': cls._engine_config.timeout_per_pass,
                'parallel_execution': cls._engine_config.parallel_execution,
                'max_functions': cls._engine_config.max_functions,
                'output_dir': cls._engine_config.output_dir,
                'save_intermediate_results': cls._engine_config.save_intermediate_results,
                'report_format': cls._engine_config.report_format,
                'enabled_passes': cls._engine_config.enabled_passes,
                'pass_config': cls._engine_config.pass_config
            },
            'logging': {
                'level': cls._logging_config.level,
                'format': cls._logging_config.format,
                'file': cls._logging_config.file,
                'console': cls._logging_config.console,
                'max_file_size': cls._logging_config.max_file_size,
                'backup_count': cls._logging_config.backup_count
            },
            'vulnerability_detection': {
                'timeout': cls._vulnerability_detection_config.timeout,
                'confidence_threshold': cls._vulnerability_detection_config.confidence_threshold,
                'max_paths': cls._vulnerability_detection_config.max_paths,
                'enable_path_optimization': cls._vulnerability_detection_config.enable_path_optimization,
                'cwe_types': cls._vulnerability_detection_config.cwe_types
            }
        }
    
    @classmethod
    def save_to_file(cls, config_file: str):
        """保存配置到文件"""
        config_path = Path(config_file)
        config_data = cls.to_dict()
        
        suffix = config_path.suffix.lower()
        
        with open(config_path, 'w', encoding='utf-8') as f:
            if suffix in ['.json']:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            elif suffix in ['.yaml', '.yml']:
                yaml.safe_dump(config_data, f, default_flow_style=False, allow_unicode=True)
            else:
                raise ValueError(f"不支持的配置文件格式: {suffix}")
        
        logging.info(f"配置已保存到: {config_file}")

# 为了向后兼容，可以保留一个简化的UnifiedConfig类型别名
UnifiedConfig = ConfigManager  # 类型别名