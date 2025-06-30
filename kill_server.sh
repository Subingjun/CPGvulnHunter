#!/bin/bash

# 检查并杀死监听 9000 到 10000 端口的进程
for port in $(seq 9000 9010); do
    # 使用 lsof 检查端口是否被占用
    pid=$(lsof -ti :$port)
    if [ -n "$pid" ]; then
        echo "发现端口 $port 被占用，进程 PID: $pid"
        # 杀死进程
        kill -9 $pid
        if [ $? -eq 0 ]; then
            echo "成功杀死进程 PID: $pid (端口: $port)"
        else
            echo "无法杀死进程 PID: $pid (端口: $port)"
        fi
    fi
done

echo "端口范围 9000 到 10000 的进程清理完成。"