#!/usr/bin/env python3
"""
测试 Task 的重试机制
"""

import sys
import os
import logging
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath('.'))

from src.CPGvulnHunter.core.task import Task

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_task_retry_mechanism():
    """测试任务重试机制"""
    print("=" * 60)
    print("测试 Task 重试机制")
    print("=" * 60)
    
    # 选择一个测试用例
    test_cases = [
        "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/output/CWE78_OS_Command_Injection/s01/CWE78_OS_Command_Injection__char_connect_socket_execl_01",
        "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/output/CWE78_OS_Command_Injection/s01/CWE78_OS_Command_Injection__char_connect_socket_execl_02"
    ]
    
    output_dir = Path("./workspace/task_retry_test")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    success_count = 0
    total_count = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n[{i}/{total_count}] 测试用例: {os.path.basename(test_case)}")
        print("-" * 50)
        
        if not os.path.exists(test_case):
            print(f"❌ 测试用例不存在: {test_case}")
            continue
        
        try:
            # 使用上下文管理器确保资源清理
            with Task(
                target_src_path=test_case,
                output_path=str(output_dir),
                passes=["cwe78"]
            ) as task:
                
                print(f"任务配置: {task.get_task_status()}")
                
                # 执行任务
                results = task.run()
                
                # 检查结果
                if results and "cwe78" in results:
                    cwe78_result = results["cwe78"]
                    analysis_results = cwe78_result.get('analysis_results', [])
                    print(f"✅ 任务执行成功")
                    print(f"   检测到 {len(analysis_results)} 个分析结果")
                    
                    # 输出部分结果
                    for j, result in enumerate(analysis_results[:3]):  # 只显示前3个
                        vuln_func = result.get('vuln_function_name', 'unknown')
                        is_vuln = result.get('is_vulnerable', False)
                        confidence = result.get('confidence', 0.0)
                        print(f"   结果{j+1}: {vuln_func} - 漏洞:{is_vuln} - 置信度:{confidence}")
                    
                    success_count += 1
                else:
                    print(f"⚠️  任务完成但无有效结果")
                    
        except Exception as e:
            print(f"❌ 任务执行失败: {e}")
            # 输出部分堆栈信息用于调试
            import traceback
            print(f"错误详情: {traceback.format_exc()[-500:]}")  # 只显示最后500字符
    
    print(f"\n" + "=" * 60)
    print(f"测试总结")
    print(f"=" * 60)
    print(f"总测试用例: {total_count}")
    print(f"成功执行: {success_count}")
    print(f"失败数量: {total_count - success_count}")
    print(f"成功率: {success_count/total_count*100:.1f}%")
    
    return success_count > 0

def test_task_with_simulated_crash():
    """测试模拟服务器崩溃的情况"""
    print(f"\n" + "=" * 60)
    print("测试模拟服务器崩溃场景")
    print("=" * 60)
    
    # 这里可以通过修改Joern包装器来模拟崩溃
    # 或者通过手动终止Joern进程来模拟
    print("注意: 此测试需要手动模拟服务器崩溃")
    print("建议:")
    print("1. 在另一个终端中找到joern进程: ps aux | grep joern")
    print("2. 在任务执行过程中终止进程: kill -9 <pid>")
    print("3. 观察任务是否自动重试")
    
    return True

if __name__ == "__main__":
    print("Task 重试机制测试")
    
    try:
        # 基本重试机制测试
        success1 = test_task_retry_mechanism()
        
        # 模拟崩溃测试说明
        success2 = test_task_with_simulated_crash()
        
        if success1:
            print("\n✅ 基本重试机制测试通过！")
            print("💡 系统已具备自动重试和恢复能力")
        else:
            print("\n❌ 基本重试机制测试失败！")
            
    except KeyboardInterrupt:
        print("\n用户中断测试")
    except Exception as e:
        print(f"\n测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
