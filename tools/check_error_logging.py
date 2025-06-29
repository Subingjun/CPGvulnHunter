#!/usr/bin/env python3
"""
检查项目中所有error日志调用是否已添加调用栈信息的脚本
"""

import os
import re
from pathlib import Path

def check_error_logging(project_root: str):
    """检查项目中的error日志调用"""
    src_dir = Path(project_root) / "src"
    
    # 查找所有Python文件
    python_files = list(src_dir.glob("**/*.py"))
    
    print("=== 检查Error日志调用 ===\n")
    
    error_calls_without_exc_info = []
    error_calls_with_exc_info = []
    
    for py_file in python_files:
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                
                for line_num, line in enumerate(lines, 1):
                    # 查找 .error( 调用
                    if re.search(r'\.error\s*\(', line):
                        # 检查是否包含 exc_info=True
                        if 'exc_info=True' in line:
                            error_calls_with_exc_info.append((py_file, line_num, line.strip()))
                        else:
                            # 排除测试文件和文档中的示例
                            if 'test' not in str(py_file).lower() and 'example' not in str(py_file).lower():
                                error_calls_without_exc_info.append((py_file, line_num, line.strip()))
                        
        except Exception as e:
            print(f"❌ 读取文件 {py_file} 失败: {e}")
    
    print(f"✅ 已添加调用栈的error调用 ({len(error_calls_with_exc_info)} 个):")
    for file_path, line_num, line in error_calls_with_exc_info:
        rel_path = file_path.relative_to(Path(project_root))
        print(f"  {rel_path}:{line_num} - {line[:80]}")
    
    print(f"\n⚠️  未添加调用栈的error调用 ({len(error_calls_without_exc_info)} 个):")
    for file_path, line_num, line in error_calls_without_exc_info:
        rel_path = file_path.relative_to(Path(project_root))
        print(f"  {rel_path}:{line_num} - {line[:80]}")
    
    print(f"\n=== 总结 ===")
    print(f"已处理的error调用: {len(error_calls_with_exc_info)}")
    print(f"需要处理的error调用: {len(error_calls_without_exc_info)}")
    
    if error_calls_without_exc_info:
        print("\n建议修改未处理的error调用，添加 exc_info=True 参数以获取调用栈信息。")
        return False
    else:
        print("\n🎉 所有error调用都已正确添加调用栈信息!")
        return True

if __name__ == "__main__":
    project_root = "/home/nstl/data/CPGvulnHunter"
    check_error_logging(project_root)
