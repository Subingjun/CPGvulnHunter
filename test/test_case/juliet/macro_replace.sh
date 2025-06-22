#!/bin/bash
# 专门用于宏替换的脚本，不包含头文件

# 设置工作目录为脚本所在目录
cd "$(dirname "$0")"

# 输入源代码目录
SOURCE_DIR="/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe"
# 输出预处理后的代码目录
OUTPUT_DIR="./macro_output"

# 创建输出目录（如果不存在）
mkdir -p "$OUTPUT_DIR"

# 定义宏替换函数
replace_macros() {
    local input_file="$1"
    local output_file="$2"
    
    # 创建临时文件用于处理
    local temp_file=$(mktemp)
    
    # 复制原文件到临时文件
    cp "$input_file" "$temp_file"
    
    # 处理条件编译指令
    # 假设我们在Linux环境下，_WIN32=0
    sed -i '/#ifdef _WIN32/,/#else \/\* NOT _WIN32 \*\//c\
/* WIN32 block removed */' "$temp_file"
    
    sed -i '/#else \/\* NOT _WIN32 \*\//,/#endif/d' "$temp_file"
    
    # 处理 OMITBAD 和 OMITGOOD
    # 如果定义了 OMITBAD，则移除 #ifndef OMITBAD 到 #endif 之间的内容
    sed -i '/#ifndef OMITBAD/,/#endif \/\* OMITBAD \*\//c\
/* BAD functions removed due to OMITBAD */' "$temp_file"
    
    # 如果定义了 OMITGOOD，则移除 #ifndef OMITGOOD 到 #endif 之间的内容  
    sed -i '/#ifndef OMITGOOD/,/#endif \/\* OMITGOOD \*\//c\
/* GOOD functions removed due to OMITGOOD */' "$temp_file"
    
    # 处理 INCLUDEMAIN
    # 保留 #ifdef INCLUDEMAIN 到 #endif 之间的内容
    sed -i '/#ifdef INCLUDEMAIN/d' "$temp_file"
    sed -i '/#endif$/d' "$temp_file"
    
    # 简单的宏替换（基于您的代码中的宏定义）
    sed -i 's/COMMAND_INT_PATH/\"\/bin\/sh\"/g' "$temp_file"
    sed -i 's/COMMAND_INT/\"sh\"/g' "$temp_file"
    sed -i 's/COMMAND_ARG1/\"-c\"/g' "$temp_file"
    sed -i 's/COMMAND_ARG2/\"ls \"/g' "$temp_file"
    sed -i 's/COMMAND_ARG3/data/g' "$temp_file"
    sed -i 's/INVALID_SOCKET/-1/g' "$temp_file"
    sed -i 's/SOCKET_ERROR/-1/g' "$temp_file"
    sed -i 's/CLOSE_SOCKET/close/g' "$temp_file"
    sed -i 's/SOCKET/int/g' "$temp_file"
    sed -i 's/TCP_PORT/27015/g' "$temp_file"
    sed -i 's/IP_ADDRESS/\"127.0.0.1\"/g' "$temp_file"
    sed -i 's/EXECL/execl/g' "$temp_file"
    
    # 移除 #include 行但保留本地包含的注释
    sed -i '/^#include </d' "$temp_file"
    sed -i 's/^#include ".*"/\/\* include removed \*\//' "$temp_file"
    
    # 移除其他预处理指令
    sed -i '/^#define/d' "$temp_file"
    sed -i '/^#pragma/d' "$temp_file"
    
    # 移除空的注释行
    sed -i '/^\/\* \*\/$/d' "$temp_file"
    
    # 输出到目标文件
    cp "$temp_file" "$output_file"
    
    # 清理临时文件
    rm "$temp_file"
}

# 遍历源代码目录中的所有 .c 和 .cpp 文件
find "$SOURCE_DIR" -type f \( -name "*.c" -o -name "*.cpp" \) | while read -r file; do
    # 获取相对路径
    RELATIVE_PATH="${file#$SOURCE_DIR/}"
    # 创建对应的输出目录
    OUTPUT_FILE="$OUTPUT_DIR/$RELATIVE_PATH"
    mkdir -p "$(dirname "$OUTPUT_FILE")"
    
    echo "Processing macros in $file -> $OUTPUT_FILE"
    replace_macros "$file" "$OUTPUT_FILE"
done

echo "Macro replacement completed. Processed files are in $OUTPUT_DIR."
