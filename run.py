from pathlib import Path
from CPGvulnHunter.core.engine import VulnerabilityEngine

def batch_run(src_path,config_file):
    base_dir = Path(src_path)
    src_paths = []
    
    # 获取所有子文件夹
    for item in base_dir.iterdir():
        if item.is_dir():
            src_paths.append(str(item))
    engine = VulnerabilityEngine(config_file=config_file)
    engine.batch_run(src_paths=src_paths, passes=['cwe78'],threads = 4)

def run(src_path, config_file):
    """
    执行漏洞分析任务
    :param src_path: 源代码路径
    :param config_file: 配置文件路径
    """
    engine = VulnerabilityEngine(config_file=config_file)
    engine.run(src_path=[src_path], passes=['cwe78'])



if __name__ == "__main__":
    # 示例：快速分析
    config_file = "config.yml"
    src_path = "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/output/CWE78_OS_Command_Injection/s01"
    batch_run(src_path,config_file)