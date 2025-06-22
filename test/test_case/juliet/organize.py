import os
import shutil
import re
"""
首先找到对应的cwe文件夹
判断是否有子文件夹（s01,s02这种）
如果没有，则根据文件名建立一个新的
"""
output_path = "./organized_cwe"


def extract_filename_prefix(filename):
    """
    提取文件名中数字之前的内容，包含数字部分
    例如: CWE78_OS_Command_Injection__char_console_execlp_52a.c
    返回: CWE78_OS_Command_Injection__char_console_execlp_52
    例如: CWE121_Stack_Based_Buffer_Overflow__CWE131_memmove_81_bad.c
    返回: CWE121_Stack_Based_Buffer_Overflow__CWE131_memmove_81
    
    :param filename: 文件名
    :return: 数字之前的前缀加上数字部分
    """
    # 移除文件扩展名
    basename = os.path.splitext(filename)[0]
    
    # 使用正则表达式匹配到数字部分（包含数字）
    # 这样 52a, 52b, 52c 都会匹配到 52，属于同一组
    match = re.match(r'^(.+_\d+)[a-z]*.*$', basename)
    if match:
        return match.group(1)
    
    # 如果没有匹配到数字，尝试匹配到最后一个下划线之前
    match = re.match(r'^(.+)_[^_]*$', basename)
    if match:
        return match.group(1)
    
    # 如果都没有匹配到，返回原始basename
    return basename


def extract_filename_prefix_alternative(filename):
    """
    提取文件名前缀的替代方法 - 按数字分组
    :param filename: 文件名
    :return: 包含数字的前缀，使同一数字的文件分在一组
    """
    # 方法2: 字符串分割方法
    basename = os.path.splitext(filename)[0]
    parts = basename.split('_')
    
    # 从后往前找第一个包含数字的部分
    for i in range(len(parts) - 1, -1, -1):
        # 检查是否包含数字（可能是纯数字或数字+字母）
        if re.search(r'\d', parts[i]):
            # 提取纯数字部分
            digit_match = re.match(r'^(\d+)', parts[i])
            if digit_match:
                # 重新构建包含数字的前缀
                return '_'.join(parts[:i] + [digit_match.group(1)])
    
    # 如果没有找到数字，返回原始basename
    return basename


def sort_cwe(cwe_path):
    """
    对cwe文件夹进行分类
    :param cwe_path: cwe文件夹路径
    :return: None
    """
    if not os.path.exists(cwe_path):
        print(f"cwe path {cwe_path} does not exist.")
        return
    output = os.path.join(output_path, os.path.basename(cwe_path))

    # 检查是否有子文件夹（如 s01, s02 等）
    subdirs = [d for d in os.listdir(cwe_path) 
               if os.path.isdir(os.path.join(cwe_path, d)) and d.startswith('s')]
    
    if subdirs:
        # 有子文件夹，只处理子文件夹，不处理根目录的文件
        print(f"发现子文件夹: {subdirs}")
        for dir_name in subdirs:
            source_dir_path = os.path.join(cwe_path, dir_name)
            output_dir_path = os.path.join(output, dir_name)
            print(f"\n处理子文件夹: {dir_name}")
            organize_testcase(source_dir_path, output_dir_path)
    else:
        # 没有子文件夹，直接处理当前目录下的文件
        print("没有发现子文件夹，直接处理根目录文件")
        organize_testcase(cwe_path, output)


def organize_testcase(source_dir, target_dir):
    """
    对测试用例进行分类
    :param source_dir: 源文件夹
    :param target_dir: 目标文件夹
    :return: None
    """
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    # 用于跟踪已处理的前缀
    processed_prefixes = set()
    
    # 典型文件名如下：CWE121_Stack_Based_Buffer_Overflow__char_type_overrun_memcpy_08.c
    # 或者：CWE121_Stack_Based_Buffer_Overflow__CWE131_memmove_81_bad.c
    # 去除掉最后一个数字之后的内容
    for file_name in os.listdir(source_dir):
        if not file_name.endswith(('.c', '.cpp', '.h')):
            continue
            
        # 提取文件名前缀
        prefix = extract_filename_prefix(file_name)
        
        # 创建基于前缀的目录
        prefix_dir = os.path.join(target_dir, prefix)
        if not os.path.exists(prefix_dir):
            os.makedirs(prefix_dir)
            print(f"创建目录: {prefix}")
        
        # 复制文件到对应目录
        source_file = os.path.join(source_dir, file_name)
        target_file = os.path.join(prefix_dir, file_name)
        
        if os.path.isfile(source_file):
            shutil.copy2(source_file, target_file)
            print(f"  复制: {file_name} -> {prefix}/")
        
        processed_prefixes.add(prefix)
    
    print(f"\n处理完成，共创建了 {len(processed_prefixes)} 个分组")


def test_extract_function():
    """
    测试提取函数
    """
    test_cases = [
        "CWE121_Stack_Based_Buffer_Overflow__char_type_overrun_memcpy_08.c",
        "CWE121_Stack_Based_Buffer_Overflow__CWE131_memmove_81_bad.c",
        "CWE121_Stack_Based_Buffer_Overflow__CWE131_memmove_81_goodG2B.c",
        "CWE78_OS_Command_Injection__char_console_execlp_52a.c",
        "CWE78_OS_Command_Injection__char_console_execlp_52b.c",
        "CWE78_OS_Command_Injection__char_console_execlp_52c.c",
        "CWE78_OS_Command_Injection__char_connect_socket_execl_22a.c",
        "CWE78_OS_Command_Injection__char_connect_socket_execl_22b.c",
        "main.cpp",
        "testcases.h"
    ]
    
    print("测试文件名前缀提取:")
    for filename in test_cases:
        prefix1 = extract_filename_prefix(filename)
        prefix2 = extract_filename_prefix_alternative(filename)
        print(f"原文件名: {filename}")
        print(f"  方法1结果: {prefix1}")
        print(f"  方法2结果: {prefix2}")
        print()


def test_organize_small_sample():
    """
    测试组织功能的小样本
    """
    # 创建测试目录和测试文件
    test_source_dir = "/tmp/test_juliet_source"
    test_target_dir = "/tmp/test_juliet_target"
    
    # 清理并创建测试目录
    if os.path.exists(test_source_dir):
        shutil.rmtree(test_source_dir)
    if os.path.exists(test_target_dir):
        shutil.rmtree(test_target_dir)
    
    os.makedirs(test_source_dir)
    
    # 创建测试文件
    test_files = [
        "CWE78_OS_Command_Injection__char_console_execlp_52a.c",
        "CWE78_OS_Command_Injection__char_console_execlp_52b.c", 
        "CWE78_OS_Command_Injection__char_console_execlp_52c.c",
        "CWE78_OS_Command_Injection__char_connect_socket_execl_22a.c",
        "CWE78_OS_Command_Injection__char_connect_socket_execl_22b.c",
        "CWE121_Stack_Based_Buffer_Overflow__CWE131_memmove_81_bad.c",
        "CWE121_Stack_Based_Buffer_Overflow__CWE131_memmove_81_goodG2B.c",
    ]
    
    # 创建空的测试文件
    for filename in test_files:
        with open(os.path.join(test_source_dir, filename), 'w') as f:
            f.write(f"// Test file: {filename}\n")
    
    print(f"创建了测试文件在: {test_source_dir}")
    print("开始组织测试...")
    
    # 执行组织
    organize_testcase(test_source_dir, test_target_dir)
    
    # 查看结果
    print(f"\n组织结果 (目标目录: {test_target_dir}):")
    for root, dirs, files in os.walk(test_target_dir):
        level = root.replace(test_target_dir, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            print(f"{subindent}{file}")


if __name__ == "__main__":

    cwe78_path = '/home/nstl/data/CPGvulnHunter/test/test_case/juliet/C/testcases/CWE78_OS_Command_Injection'
    sort_cwe(cwe78_path)