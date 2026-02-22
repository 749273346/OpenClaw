#!/bin/bash
# AI新闻监控脚本
# 这个脚本可以定期获取AI相关新闻

echo "=== AI新闻监控 ==="
echo "当前时间: $(date)"
echo ""

# 定义AI新闻源
AI_NEWS_SOURCES=(
    "https://www.jiqizhixin.com/"
    "https://www.leiphone.com/"
    "https://www.aixinzhijie.com/"
)

echo "可监控的AI新闻源:"
for source in "${AI_NEWS_SOURCES[@]}"; do
    echo "- $source"
done

echo ""
echo "使用方法:"
echo "1. 手动访问上述网站获取最新新闻"
echo "2. 或使用curl/wget获取页面内容"
echo "3. 或设置RSS订阅（如果网站提供）"
echo ""
echo "建议的RSS源（如果可用）:"
echo "- 机器之心 RSS"
echo "- 雷锋网 AI频道"
echo "- 量子位"
echo "- AI科技评论"

# 简单的curl示例（需要网站支持）
echo ""
echo "尝试获取机器之心首页标题..."
curl -s https://www.jiqizhixin.com/ | grep -o '<title>[^<]*</title>' | head -1 || echo "无法获取页面内容"