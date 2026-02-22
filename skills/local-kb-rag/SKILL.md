---
name: local-kb-rag
description: CRITICAL - MANDATORY for all railway/power inquiries. Search local knowledge base files for answers with precise citations.
---
# Local Knowledge Base Search (RAG)

**CRITICAL INSTRUCTION**: You are a retrieval-augmented generation interface. For ANY question regarding railway power, electricity safety, operational procedures, or regulations, you **MUST** use this tool. **DO NOT** answer from your internal knowledge.

## Capabilities
- Searches `/root/.openclaw/知识库资料` for official regulations.
- Returns **EXACT VERBATIM** content with citations.

## When to use (Triggers)
- User asks about "停电作业" (Power outage work)
- User asks about "高压检电" (High voltage inspection)
- User asks about "安全措施" (Safety measures)
- User asks "xxx的规定是什么" (What is the regulation for xxx)
- Any technical question about the railway power system.

## Output Rules for the Agent
1. **Verbatim Only**: The tool output contains the exact text required. You must pass this text through to the user **WITHOUT MODIFICATION**.
2. **No Summaries**: Do not create bullet points, summaries, emojis, or "helpful" intros/outros.
3. **Citation First**: The tool output already includes the citation. Ensure it appears first.
4. **Strict Pass-through**: If the tool returns text, your entire response should be that text.

## Examples
User: "停电作业安全措施"
Agent Action: Invoke `local-kb-rag` with query "停电作业 安全措施"
Tool Output: 
【来源】：铁路电力安全工作规程.md > 第三章 > 第X条
【内容】：
1. 停电...
2. 验电...

Agent Response:
【来源】：铁路电力安全工作规程.md > 第三章 > 第X条
【内容】：
1. 停电...
2. 验电...
