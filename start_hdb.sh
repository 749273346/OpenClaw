#!/bin/bash
# 惠电宝启动脚本 (Start Script - PM2 Managed)

# 切换到 OpenClaw 工作目录
cd /root/.openclaw
mkdir -p logs

echo "正在检查环境..."

# 检查是否有非 PM2 管理的 openclaw gateway 进程
# 如果 pm2 list 中没有 hdb-agent，但 pgrep 发现了 openclaw gateway，说明有残留进程
RUNNING_PID=$(pgrep -f "openclaw gateway")
PM2_STATUS=$(pm2 jlist | grep "hdb-agent")

if [ -n "$RUNNING_PID" ] && [ -z "$PM2_STATUS" ]; then
    echo "警告: 发现非 PM2 管理的 OpenClaw 进程 (PID: $RUNNING_PID)。"
    echo "正在尝试停止它..."
    kill $RUNNING_PID
    sleep 2
fi

# 启动或重启 PM2 任务
if pm2 list | grep -q "hdb-agent"; then
    echo "hdb-agent 已经在 PM2 列表中，正在重启..."
    pm2 restart hdb-agent
else
    echo "正在启动 hdb-agent (PM2)..."
    pm2 start ecosystem.config.js
fi

# 保存当前 PM2 列表以便开机自启（如果配置了 startup）
pm2 save

echo "启动指令已发送！"
echo "日志文件: /root/.openclaw/logs/pm2-out.log"
echo "使用 ./logs_hdb.sh 查看实时日志"
