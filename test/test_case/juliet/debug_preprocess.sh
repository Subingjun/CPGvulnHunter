#!/bin/bash
# 调试版本预处理脚本 - 显示错误信息
cd "$(dirname "$0")"

SOURCE_DIR="/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe"
OUTPUT_DIR="./debug_output"
INCLUDE_DIR="/home/nstl/data/CPGvulnHunter/test/test_case/juliet/C/testcasesupport/"
MINIMAL_HEADERS_DIR="/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/"

mkdir -p "$OUTPUT_DIR"

# 只测试前20个失败的文件
echo "=== 分析预处理失败的原因 ==="
FAILED_COUNT=0
ANALYZED_COUNT=0

find "$SOURCE_DIR" -type f \( -name "*.c" -o -name "*.cpp" \) | while read -r file; do
    RELATIVE_PATH="${file#$SOURCE_DIR/}"
    OUTPUT_FILE="$OUTPUT_DIR/$RELATIVE_PATH"
    mkdir -p "$(dirname "$OUTPUT_FILE")"
    
    # 测试预处理
    if ! gcc -E -nostdinc -I"$MINIMAL_HEADERS_DIR" -I"$INCLUDE_DIR" -DOMITBAD -DINCLUDEMAIN "$file" > "$OUTPUT_FILE" 2>"$OUTPUT_FILE.err"; then
        echo "=== 失败文件: $(basename "$file") ==="
        echo "错误信息:"
        head -5 "$OUTPUT_FILE.err"
        echo "---"
        FAILED_COUNT=$((FAILED_COUNT + 1))
        
        if [ $FAILED_COUNT -ge 10 ]; then
            echo "已分析10个失败文件，停止..."
            break
        fi
    else
        rm -f "$OUTPUT_FILE.err"
    fi
    
    ANALYZED_COUNT=$((ANALYZED_COUNT + 1))
    if [ $ANALYZED_COUNT -ge 100 ]; then
        echo "已分析100个文件，停止..."
        break
    fi
done
