---
name: ai-news-summarizer
description: AI新闻总结器 - 获取和总结AI领域的最新新闻
version: 1.0.0
author: OpenClaw Assistant
created: 2026-02-22
---

# AI新闻总结器技能

## 功能
- 获取AI领域的最新新闻
- 总结关键信息
- 提供新闻来源链接

## 使用方法
当用户请求"总结本周AI大事"或类似请求时，使用此技能。

## 实现步骤
1. 收集AI新闻源
2. 获取最新新闻标题和摘要
3. 总结关键趋势和事件
4. 格式化输出

## 新闻源
- 机器之心: https://www.jiqizhixin.com/
- 雷锋网: https://www.leiphone.com/
- AI科技评论
- VentureBeat AI
- MIT Technology Review AI

## 命令示例
```bash
# 获取AI新闻摘要
./ai_news_summary.sh
```

## 依赖
- curl或wget
- Python 3.x（可选，用于更复杂的解析）