# MEMORY.md - 长期记忆

这是OpenClaw助手的长期记忆文件。包含重要的学习、决定、偏好和经验教训。

## 身份信息
- **助手名称**: 小爪 (暂定，待用户确认)
- **风格**: 温暖、乐于助人、直接
- **表情符号**: 🦞
- **创建日期**: 2026-02-22

## 用户信息
- **姓名**: YangHao
- **联系渠道**: 企业微信(WeCom)
- **兴趣**: 
  - AI新闻、自动化工具
  - 铁路电力安全规程（如倒闸操作）
- **待确认**: 时区、称呼偏好

## 订阅用户
- **ShiShuiLiuNian**: 2026-02-24订阅，已发送欢迎消息，等待用户回复确认身份和需求
- **usualmind**: 2026-02-25订阅，企业微信用户，订阅事件已记录，等待用户主动发起对话

## 重要学习
1. **AI新闻需求**: 用户需要定期获取AI领域新闻摘要
2. **铁路电力安全需求**: 用户对铁路电力安全规程感兴趣
3. **技能发现**: volcengine-kb技能可用于铁路电力安全规程查询
4. **工具限制**: web_search需要Brave API密钥，blogwatcher工具未安装

## 技术环境
- Python 3.11.6已安装，但pip3不可用
- volcengine-kb技能可用，API密钥已配置
- 需要通过配置或替代方案解决新闻获取问题

## 创建的资源
1. `ai_news_monitor.sh` - AI新闻监控脚本
2. `skills/ai-news-summarizer/` - AI新闻总结技能目录
3. `skills/volcengine-kb/` - 火山引擎知识库技能
4. 更新的配置文件: IDENTITY.md, USER.md

## 成功案例
- 使用volcengine-kb技能成功查询"倒闸操作"相关规定
- 为用户提供了详细的铁路电力安全规程信息

## 待办事项
- 确认用户时区信息
- 确认助手名称'小爪'是否合适
- 探索AI新闻获取的替代方案
- 考虑设置定期AI新闻摘要任务
- 探索更多铁路电力安全相关的查询需求

## 教训
- 在创建技能前检查工具可用性
- 尽早收集用户偏好信息（时区、称呼等）
- 记录技术限制以便寻找解决方案
- 发现用户潜在需求领域（铁路电力安全）

### 3. 多模态能力 (Multimodal Capabilities)
- **实现方案**: 
  - **移动端兼容**: 针对企业微信移动端图片消息，采用 **Visual Pre-processing Pipeline** 架构。
  - **直接调用**: `agent/handler.ts` 拦截图片消息，直接调用 `ask_volcengine.py --analyze-only` 获取视觉描述。
  - **上下文注入**: 将分析结果以 `[系统注入: 图片分析结果 (Visual Analysis)]` 格式注入到用户消息末尾。
  - **LLM 感知**: 核心 LLM (DeepSeek/Doubao) 接收到的不再是单纯的 `[FILE_PATH]`，而是包含详细视觉描述的文本，从而能够回答相关问题。
- **流程**: 
  1. 用户发送图片 -> WeCom Handler 接收。
  2. Handler 检测到图片 -> 调用 Python 脚本 (Zhipu GLM-4V) 分析。
  3. Python 脚本输出结构化描述 (Description, Related, Reasoning, Answer)。
  4. Handler 将描述追加到 `finalContent`。
  5. `finalContent` 发送给 OpenClaw Core -> LLM 处理 -> 返回结果。
- **优势**: 
  - 规避了 LLM Tool Use 的不稳定性。
  - 解决了移动端图片路径传递和权限问题。
  - 降低了多轮对话的延迟（图片分析在接收时即完成）。

### 4. 知识库 (Knowledge Base)
