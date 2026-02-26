#!/bin/bash
# 惠电宝停止脚本 (Stop Script - PM2 Managed)

echo "正在停止惠电宝..."

# 停止 PM2 任务
if pm2 list | grep -q "hdb-agent"; then
    pm2 stop hdb-agent
    echo "PM2 任务已停止。"
else
    echo "未发现 PM2 管理的 hdb-agent。"
fi

# 检查残留进程
PID=$(pgrep -f "openclaw gateway")
if [ -n "$PID" ]; then
    echo "发现残留进程 PID: $PID，正在清理..."
    kill $PID
    sleep 1
fi

echo "停止完成。"
