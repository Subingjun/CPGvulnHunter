#!/usr/bin/env python3
"""
演示Task重试机制的概念验证
"""

import time
import logging

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class MockTask:
    """模拟Task类来演示重试机制"""
    
    def __init__(self, target_path: str):
        self.target_path = target_path
        self.max_task_retries = 3
        self.current_retry = 0
        self.logger = logging.getLogger(__name__)
        
    def run(self):
        """带重试机制的任务执行"""
        for retry_count in range(self.max_task_retries + 1):
            try:
                self.current_retry = retry_count
                if retry_count > 0:
                    self.logger.warning(f"任务重试 {retry_count}/{self.max_task_retries}")
                    time.sleep(2)  # 模拟重启等待时间
                
                return self._execute_task()
                
            except Exception as e:
                error_msg = str(e)
                
                # 检查是否是服务器崩溃
                if self._is_server_crash_error(error_msg):
                    self.logger.error(f"检测到服务器崩溃: {error_msg}")
                    
                    if retry_count < self.max_task_retries:
                        self.logger.info(f"准备重试任务 ({retry_count + 1}/{self.max_task_retries})...")
                        continue
                    else:
                        self.logger.error(f"任务重试次数已达上限，任务失败")
                        raise RuntimeError(f"任务在{self.max_task_retries}次重试后仍然失败")
                else:
                    # 非服务器崩溃错误，直接抛出
                    raise
    
    def _execute_task(self):
        """模拟任务执行"""
        self.logger.info(f"开始执行任务: {self.target_path}")
        
        # 模拟不同的情况
        import random
        scenario = random.choice([
            "success",           # 成功
            "server_crash",      # 服务器崩溃
            "other_error"        # 其他错误
        ])
        
        if scenario == "success":
            self.logger.info("任务执行成功")
            return {"status": "success", "results": ["result1", "result2"]}
        elif scenario == "server_crash":
            raise RuntimeError("JOERN_SERVER_CRASHED: 模拟服务器崩溃")
        else:
            raise RuntimeError("模拟其他类型的错误")
    
    def _is_server_crash_error(self, error_msg: str) -> bool:
        """判断是否是服务器崩溃错误"""
        crash_indicators = [
            "JOERN_SERVER_CRASHED",
            "连续超时",
            "服务器崩溃",
            "OutOfMemoryError",
            "StackOverflowError"
        ]
        
        error_lower = error_msg.lower()
        return any(indicator.lower() in error_lower for indicator in crash_indicators)

def demo_retry_mechanism():
    """演示重试机制"""
    print("=" * 60)
    print("Task 重试机制演示")
    print("=" * 60)
    
    test_cases = [
        "test_case_1",
        "test_case_2", 
        "test_case_3"
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n[{i}/{len(test_cases)}] 测试用例: {test_case}")
        print("-" * 40)
        
        try:
            task = MockTask(test_case)
            result = task.run()
            print(f"✅ 任务成功: {result}")
            
        except Exception as e:
            print(f"❌ 任务最终失败: {e}")
    
    print(f"\n" + "=" * 60)
    print("重试机制概念验证完成")
    print("=" * 60)
    print("主要特性:")
    print("1. 自动检测服务器崩溃错误")
    print("2. 最多重试3次")
    print("3. 非崩溃错误直接失败")
    print("4. 重试间有等待时间")
    print("5. 完整的日志记录")

if __name__ == "__main__":
    demo_retry_mechanism()
