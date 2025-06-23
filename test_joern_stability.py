#!/usr/bin/env python3
"""
Joern连接稳定性测试脚本
用于测试超时重传机制和连接稳定性
"""

import time
import logging
import sys
import os

# 添加项目路径
sys.path.insert(0, '/home/nstl/data/CPGvulnHunter/src')

from CPGvulnHunter.bridges.joernBridge import JoernBridge
from CPGvulnHunter.bridges.joernWrapper import JoernWrapper

def setup_logging():
    """设置日志"""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('joern_test.log', encoding='utf-8')
        ]
    )

def test_basic_connection():
    """测试基本连接"""
    print("=" * 50)
    print("测试基本连接...")
    
    try:
        bridge = JoernBridge()
        
        # 测试简单命令
        result = bridge.send_command("1 + 1")
        print(f"基本测试结果: {result}")
        
        # 测试健康检查
        health = bridge.health_check()
        print(f"健康检查: {health}")
        
        # 获取状态
        status = bridge.get_status()
        print(f"连接状态: {status}")
        
        bridge.close_shell()
        print("基本连接测试完成")
        
    except Exception as e:
        print(f"基本连接测试失败: {e}")

def test_timeout_retry():
    """测试超时重传机制"""
    print("=" * 50)
    print("测试超时重传机制...")
    
    try:
        wrapper = JoernWrapper()
        
        # 测试短超时的命令（应该成功）
        print("测试短超时命令...")
        result = wrapper._execute_command("1 + 1", timeout=5)
        print(f"短超时测试结果: {result}")
        
        # 测试较复杂的命令
        print("测试复杂命令...")
        result = wrapper._execute_command('val test = List(1,2,3,4,5)', timeout=30)
        print(f"复杂命令测试结果: {result}")
        
        wrapper.close()
        print("超时重传测试完成")
        
    except Exception as e:
        print(f"超时重传测试失败: {e}")

def test_import_code():
    """测试代码导入功能"""
    print("=" * 50)
    print("测试代码导入功能...")
    
    # 使用你提到的测试路径
    test_path = "/home/nstl/data/CPGvulnHunter/test/test_case/test4/CWE78_OS_Command_Injection__char_connect_socket_execl_02"
    
    if not os.path.exists(test_path):
        print(f"测试路径不存在: {test_path}")
        return
    
    try:
        wrapper = JoernWrapper()
        
        print(f"开始导入代码: {test_path}")
        start_time = time.time()
        
        # 导入代码（使用较长的超时时间）
        wrapper.import_code(test_path)
        
        duration = time.time() - start_time
        print(f"代码导入完成，耗时: {duration:.2f}秒")
        
        # 获取函数列表
        print("获取函数列表...")
        functions = wrapper.get_function_full_names()
        if functions:
            print(f"找到 {len(functions)} 个函数:")
            for func in functions[:5]:  # 只显示前5个
                print(f"  - {func}")
            if len(functions) > 5:
                print(f"  ... 还有 {len(functions) - 5} 个函数")
        else:
            print("未找到函数")
        
        wrapper.close()
        print("代码导入测试完成")
        
    except Exception as e:
        print(f"代码导入测试失败: {e}")
        import traceback
        traceback.print_exc()

def main():
    """主函数"""
    setup_logging()
    
    print("Joern连接稳定性测试开始")
    print("=" * 50)
    
    # 运行各项测试
    test_basic_connection()
    time.sleep(2)
    
    test_timeout_retry()
    time.sleep(2)
    
    test_import_code()
    
    print("=" * 50)
    print("所有测试完成")

if __name__ == "__main__":
    main()
