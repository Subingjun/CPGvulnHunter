#!/usr/bin/env python3
"""
测试 JoernBridge 的自动重启功能
"""

import sys
import os
import time
import logging

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath('.'))

from src.CPGvulnHunter.bridges.joernBridge import JoernBridge

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_joern_restart():
    """测试 Joern 服务器的自动重启功能"""
    print("开始测试 Joern 服务器自动重启功能...")
    
    try:
        # 第一次启动
        print("\n=== 第一次启动 JoernBridge ===")
        with JoernBridge() as bridge1:
            print("第一个实例启动成功")
            
            # 测试基本功能
            result = bridge1.send_command("1 + 1")
            print(f"测试命令结果: {result}")
            
            # 获取状态
            status = bridge1.get_status()
            print(f"服务器状态: {status}")
        
        print("第一个实例已关闭")
        
        # 稍等一下
        time.sleep(2)
        
        # 第二次启动（应该会强制重启服务器）
        print("\n=== 第二次启动 JoernBridge ===")
        with JoernBridge() as bridge2:
            print("第二个实例启动成功")
            
            # 测试基本功能
            result = bridge2.send_command("2 + 2")
            print(f"测试命令结果: {result}")
            
            # 健康检查
            health = bridge2.health_check()
            print(f"健康检查结果: {health}")
        
        print("第二个实例已关闭")
        print("\n测试完成！所有功能正常工作")
        
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def test_concurrent_instances():
    """测试并发实例的处理"""
    print("\n=== 测试并发实例处理 ===")
    
    try:
        # 启动第一个实例
        bridge1 = JoernBridge()
        print("第一个实例启动成功")
        
        # 尝试启动第二个实例（应该会终止第一个服务器并启动新的）
        bridge2 = JoernBridge()
        print("第二个实例启动成功")
        
        # 测试第二个实例
        result = bridge2.send_command("3 + 3")
        print(f"第二个实例测试结果: {result}")
        
        # 清理
        bridge1.close_shell()
        bridge2.close_shell()
        
        print("并发测试完成")
        return True
        
    except Exception as e:
        print(f"并发测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("JoernBridge 重启功能测试")
    print("=" * 50)
    
    # 基本重启测试
    success1 = test_joern_restart()
    
    # 并发实例测试
    success2 = test_concurrent_instances()
    
    if success1 and success2:
        print("\n✅ 所有测试通过！")
        sys.exit(0)
    else:
        print("\n❌ 测试失败！")
        sys.exit(1)
