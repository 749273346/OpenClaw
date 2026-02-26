#!/bin/bash
# 惠电宝日志查看脚本 (Log Viewer - PM2 Managed)

echo "正在查看惠电宝实时日志 (Ctrl+C 退出)..."
pm2 logs hdb-agent --lines 50
