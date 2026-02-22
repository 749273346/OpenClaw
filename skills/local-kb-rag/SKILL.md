---
name: local-kb-rag
description: Search local knowledge base files for answers with precise citations (File > Chapter > Section).
---

# Local Knowledge Base Search

This skill searches the local knowledge base directory `/root/.openclaw/知识库资料` for relevant information to answer user questions.

## Capabilities

- **Search**: Finds relevant sections based on keywords.
- **Citation**: Provides the source file, chapter, and section for every answer.
- **Context**: Returns the content snippet to help generate a comprehensive answer.

## Usage

Invoke this skill when the user asks a question about:
- Railway power safety regulations (铁路电力安全工作规程)
- Railway power management rules (铁路电力管理规则)
- High-speed railway power management (高速铁路电力管理规则)
- Any question requiring lookup in the local KB.

## Example

**User:** "工作票制度有哪些规定？"

**Assistant:** (Calls `local-kb-rag` with query "工作票制度")

**Skill Output:**
```
Found 3 matches for '工作票制度':

--- Match 1 ---
Source: 铁路电力安全工作规程.md
Location: 第二章 保证安全工作的组织措施 > 第一节 工作票制度
Content:
... (content snippet) ...
```

## Implementation

The skill uses a Python script `search_kb.py` to parse Markdown headers and perform keyword matching.
