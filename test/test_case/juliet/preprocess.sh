#!/bin/bash
# 设置工作目录为脚本所在目录
cd "$(dirname "$0")"

# 输入源代码目录
SOURCE_DIR="/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe"
# 输出预处理后的代码目录
OUTPUT_DIR="./output"
# 包含头文件的目录
INCLUDE_DIR="/home/nstl/data/CPGvulnHunter/test/test_case/juliet/C/testcasesupport/"
# 最小化头文件目录
MINIMAL_HEADERS_DIR="/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/"

# 创建输出目录（如果不存在）
mkdir -p "$OUTPUT_DIR"

# 统计变量
TOTAL_FILES=0
SUCCESS_FILES=0
FAILED_FILES=0

# 遍历源代码目录中的所有 .c 和 .cpp 文件
find "$SOURCE_DIR" -type f \( -name "*.c" -o -name "*.cpp" \) | while read -r file; do
    # 获取相对路径
    RELATIVE_PATH="${file#$SOURCE_DIR/}"
    # 创建对应的输出目录
    OUTPUT_FILE="$OUTPUT_DIR/$RELATIVE_PATH"
    mkdir -p "$(dirname "$OUTPUT_FILE")"

    # 统计总文件数
    TOTAL_FILES=$((TOTAL_FILES + 1))

    # 预处理文件，进行宏替换并包含头文件
    echo "Preprocessing $file -> $OUTPUT_FILE"
    
    # 使用 -nostdinc 避免包含标准头文件，使用最小化头文件
    if gcc -E \
        -nostdinc \
        -I"$MINIMAL_HEADERS_DIR" \
        -I"$INCLUDE_DIR" \
        -DOMITBAD \
        -DINCLUDEMAIN \
        "$file" 2>/dev/null > "$OUTPUT_FILE"; then
        echo "  ✓ Success"
        SUCCESS_FILES=$((SUCCESS_FILES + 1))
    else
        echo "  ✗ Skipped (preprocessing failed)"
        rm -f "$OUTPUT_FILE"
        FAILED_FILES=$((FAILED_FILES + 1))
    fi
done

echo "Preprocessing completed. Preprocessed files are in $OUTPUT_DIR."

# 统计结果
echo ""
echo "=== Preprocessing Statistics ==="
find "$SOURCE_DIR" -type f \( -name "*.c" -o -name "*.cpp" \) | wc -l | { read total; echo "Total files found: $total"; }
find "$OUTPUT_DIR" -type f \( -name "*.c" -o -name "*.cpp" \) | wc -l | { read success; echo "Successfully preprocessed: $success"; }
echo "Check the output directory for preprocessed files."