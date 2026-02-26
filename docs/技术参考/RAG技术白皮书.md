# 惠电宝 - 检索增强技术白皮书 (RAG Technical Whitepaper)

## 1. 背景 (Background)
在铁路电力安全领域，规程繁多且专业性极强。传统的关键词搜索难以理解“变压器检修”与“变压器维护”的等价性，也无法处理“昨天的故障”等上下文依赖问题。惠电宝引入了基于 Hybrid Search 的 RAG（Retrieval-Augmented Generation）架构，旨在提供精准、权威的智能问答服务。

## 2. 技术架构 (Technical Architecture)

### 2.1 混合检索 (Hybrid Retrieval)
我们采用了 BM25 + Dense Retrieval 的双路召回策略：
- **BM25 (Sparse Retrieval)**:
  - **原理**: 基于词频（TF-IDF）的倒排索引算法。
  - **优势**: 对专有名词（如“接触网”、“隔离开关”）、数字（“110kV”）极其敏感。
  - **实现**: 使用 `rank_bm25` 库，配合 `jieba` 中文分词。
- **Dense Retrieval (Semantic Search)**:
  - **原理**: 将文本映射为高维向量（Embedding），通过计算余弦相似度（Cosine Similarity）衡量语义距离。
  - **模型**: Zhipu AI `embedding-3` (2048维)。
  - **优势**: 能够理解同义词、上下文隐含意义。
  - **实现**: 使用 `zhipuai` SDK 生成向量，`numpy` 进行相似度计算。

### 2.2 重排序与融合 (Re-ranking & Fusion)
为了平衡两路检索的优缺点，我们采用了加权融合（Weighted Fusion）策略：
```python
final_score = alpha * normalize(bm25_score) + (1 - alpha) * normalize(semantic_score)
```
目前 `alpha` 设定为 **0.3**，即更偏重语义理解，但在精确匹配专有名词时 BM25 仍起关键作用。

### 2.3 生成增强 (Generation Augmentation)
检索到的 Top-K 文档片段（Chunks）被组装进 Prompt Context，输送给 DeepSeek 大模型。我们设计了结构化的 System Prompt，强制模型：
- **基于事实**: 仅使用 Context 中的内容回答，严禁幻觉。
- **引用溯源**: 每个观点必须标注 `> 来源：[文件名] 第N条`。
- **格式规范**: 强制使用 Markdown 表格展示数据对比。

## 3. 索引构建 (Indexing Strategy)

### 3.1 文本分块 (Chunking)
- **策略**: 基于 Markdown 标题（Headers）进行语义分块。
- **粒度**: 保持完整的章节（Section）作为一个 Chunk，避免断章取义。
- **元数据**: 每个 Chunk 包含 `filename`（来源书名）和 `header`（章节标题），便于引用。

### 3.2 向量化 (Vectorization)
- **预处理**: 文本长度截断（防止 API 报错），去除无意义字符。
- **存储**: 使用 Pickle 序列化存储 `(chunks, embeddings, bm25_object)`，简单高效，适合中小规模知识库（<10万条）。

## 4. 性能与优化 (Performance & Optimization)
- **响应速度**: 本地索引加载毫秒级，Embedding API 调用约 200-500ms，整体检索耗时 <1s。
- **并发控制**: 索引构建时采用批处理与错误重试机制，确保稳定性。
- **冷启动**: 首次运行需全量构建索引，后续可支持增量更新（待实现）。

## 5. 未来规划 (Future Roadmap)
- **多路召回**: 引入 Query Expansion（查询扩展）与 Hypothetical Document Embeddings (HyDE)。
- **精细化重排**: 引入 Cross-Encoder 模型（如 BGE-Reranker）进行二次精排。
- **知识图谱**: 构建电力设备实体关系图谱，支持多跳推理。

---
*文档维护者: 惠电宝-算法团队*
*最后更新: 2026-02-23*
