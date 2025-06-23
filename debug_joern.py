#!/usr/bin/env python3
"""
简单的 JoernBridge 测试
"""

import sys
import os
import logging

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath('.'))

# 设置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

try:
    from src.CPGvulnHunter.core.config import ConfigManager
    
    print("测试配置管理器...")
    config_manager = ConfigManager()
    joern_config = config_manager.get_joern_config()
    
    print(f"Joern 路径: {joern_config.installation_path}")
    print(f"超时时间: {joern_config.timeout}")
    print(f"服务器端点: {joern_config.server_endpoint}")
    
    # 测试 JoernBridge
    print("\n测试 JoernBridge 初始化...")
    from src.CPGvulnHunter.bridges.joernBridge import JoernBridge
    
    # 首先终止现有的 Joern 服务器
    import subprocess
    import time
    
    try:
        subprocess.run(['pkill', '-f', 'joern.*--server'], timeout=5)
        time.sleep(2)
        print("已终止现有的 Joern 服务器")
    except:
        print("无现有 Joern 服务器需要终止")
    
    # 使用显式参数
    bridge = JoernBridge(
        joern_path="/home/nstl/data/CPGvulnHunter/joern-cli/joern",
        timeout=120,
        server_endpoint="localhost:8080"
    )
    
    print("JoernBridge 初始化成功！")
    
    # 测试基本命令
    result = bridge.send_command("1 + 1")
    print(f"测试命令结果: {result}")
    
    # 清理
    bridge.close_shell()
    print("测试完成！")
    
except Exception as e:
    print(f"测试失败: {e}")
    import traceback
    traceback.print_exc()
