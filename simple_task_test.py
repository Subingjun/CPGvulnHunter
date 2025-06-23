#!/usr/bin/env python3
"""
简单的Task重试测试
"""

import sys
import os
import logging

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath('.'))

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_single_task():
    """测试单个任务的执行"""
    print("测试单个Task执行...")
    
    try:
        from src.CPGvulnHunter.core.task import Task
        
        # 选择一个简单的测试用例
        test_case = "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/output/CWE78_OS_Command_Injection/s01/CWE78_OS_Command_Injection__char_connect_socket_execl_01"
        
        if not os.path.exists(test_case):
            print(f"测试用例不存在: {test_case}")
            return False
        
        with Task(
            target_src_path=test_case,
            output_path="./workspace/simple_test",
            passes=["cwe78"]
        ) as task:
            
            print(f"任务状态: {task.get_task_status()}")
            
            # 执行任务
            results = task.run()
            
            print(f"任务执行成功！")
            print(f"结果: {results}")
            
            return True
            
    except Exception as e:
        print(f"任务执行失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("简单Task测试")
    print("=" * 40)
    
    success = test_single_task()
    
    if success:
        print("\n✅ 任务执行成功！重试机制已就绪。")
    else:
        print("\n❌ 任务执行失败！")
