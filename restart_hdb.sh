#!/bin/bash
# 惠电宝重启脚本 (Restart Script - PM2 Managed)

echo "正在重启惠电宝..."

# 检查 PM2 是否存在
if pm2 list | grep -q "hdb-agent"; then
    pm2 restart hdb-agent
else
    echo "未发现 PM2 管理的 hdb-agent，正在启动..."
    ./start_hdb.sh
fi

echo "重启完成。"
echo "日志文件: /root/.openclaw/logs/pm2-out.log"
echo "使用 ./logs_hdb.sh 查看实时日志"
