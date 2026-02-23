# HDB RAG Skill (DeepSeek/Zhipu Powered)

This skill allows the agent to query the local Huidianbao Knowledge Base for precise answers about railway power supply safety regulations and operational procedures. It uses DeepSeek for reasoning/chat and Zhipu AI for image analysis.

**NEW: Enhanced with Hybrid Search (BM25 + Semantic) for higher recall and precision.**

## When to use
- Use this skill for ANY question related to:
  - Railway power supply safety (铁路电力安全)
  - Operational procedures (作业流程)
  - Safety regulations (安全规程)
  - Emergency handling (应急处理)
  - Technical specifications (技术规范)
  - **Image Analysis**: Identify and analyze railway power equipment, defects, or scenes from uploaded images.
- Even for simple questions like "What is X?", prefer using this skill to get an authoritative answer from the Knowledge Base.

## Parameters
- `query`: The user's question or search query. Can include `[FILE_PATH: /path/to/image]` for image analysis.

## Maintenance
- **Rebuild Index**: If knowledge base files change, run `python3 /root/.openclaw/build_kb_index.py` to update the search index.

## Returns
- A markdown-formatted answer with citations from the Knowledge Base.
