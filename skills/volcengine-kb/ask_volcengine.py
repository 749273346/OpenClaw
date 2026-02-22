
import os
import json
import sys
import glob
from volcenginesdkarkruntime import Ark

import re
from collections import Counter

# Configuration
KB_DIR = "/root/.openclaw/知识库资料"
API_KEY = "99073b82-9920-42ea-92d1-7b75a1e3f274"
ENDPOINT_ID = "ep-m-20260222201045-gvjbn"

def chunk_markdown(content, filename):
    """
    Split markdown content into logical chunks based on headers.
    Returns a list of dicts: {'content': str, 'source': str, 'score': 0}
    """
    chunks = []
    lines = content.split('\n')
    current_chunk = []
    current_header = ""
    
    for line in lines:
        if line.strip().startswith('#'):
            # New section starts, save previous chunk if not empty
            if current_chunk:
                full_text = "\n".join(current_chunk).strip()
                if full_text:
                    chunks.append({
                        'content': f"--- 来源：{filename} {current_header} ---\n{full_text}",
                        'source': filename,
                        'text_only': full_text
                    })
            current_chunk = [line]
            current_header = line.strip()
        else:
            current_chunk.append(line)
            
    # Add last chunk
    if current_chunk:
        full_text = "\n".join(current_chunk).strip()
        if full_text:
            chunks.append({
                'content': f"--- 来源：{filename} {current_header} ---\n{full_text}",
                'source': filename,
                'text_only': full_text
            })
            
    return chunks

def score_chunks(chunks, query):
    """
    Score chunks based on keyword overlap with query.
    Simple term frequency scoring.
    """
    # Tokenize query (simple char-based or jieba-like if available, here char-based n-grams for Chinese)
    # For simplicity, just use character overlap and exact phrase matching
    query_terms = set(query)
    query_phrases = [query[i:i+2] for i in range(len(query)-1)] # Bi-grams
    
    for chunk in chunks:
        text = chunk['text_only']
        score = 0
        # Exact phrase match bonus
        if query in text:
            score += 50
        
        # Bi-gram match
        for phrase in query_phrases:
            if phrase in text:
                score += 5
                
        # Character match
        for char in query_terms:
            if char in text:
                score += 1
                
        chunk['score'] = score
        
    return sorted(chunks, key=lambda x: x['score'], reverse=True)

def load_relevant_context(query, top_k=15):
    """
    Load MD files, chunk them, score them, and return top_k chunks.
    """
    all_chunks = []
    try:
        if not os.path.exists(KB_DIR):
            return ""
        
        files = glob.glob(os.path.join(KB_DIR, "*.md"))
        for file_path in files:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                filename = os.path.basename(file_path)
                file_chunks = chunk_markdown(content, filename)
                all_chunks.extend(file_chunks)
                
        # Score and filter
        scored_chunks = score_chunks(all_chunks, query)
        top_chunks = scored_chunks[:top_k]
        
        # Sort top chunks by book priority
        book_priority = {
            "高速铁路电力管理规则.md": 1,
            "铁路电力安全工作规程补充规定.md": 2,
            "铁路电力管理规则.md": 3,
            "铁路电力安全工作规程.md": 4
        }
        
        top_chunks.sort(key=lambda x: book_priority.get(x['source'], 99))
        
        context_str = "\n\n".join([c['content'] for c in top_chunks])
        return context_str
        
    except Exception as e:
        print(f"Error loading context: {e}", file=sys.stderr)
        return ""

def chat_with_model(query):
    """
    Primary Interaction Logic: Smart Retrieval RAG + Volcengine Ark Model
    """
    try:
        client = Ark(api_key=API_KEY)
        
        # 1. Load Relevant Knowledge Base Context (Top 5 chunks)
        # Reduce to 5 chunks to improve response speed (latency < 30s)
        context_str = load_relevant_context(query, top_k=5)
        
        if context_str:
            system_prompt = f"""
# Role
你是一位专业的“铁路电力接触网安全作业助手”。你的唯一任务是根据提供的【参考资料】回答用户关于作业流程、安全规定、操作规范等问题。

# Constraints & Rules
1. **严格基于资料**：你必须仅根据 `<context>` 标签内提供的参考资料回答问题。
2. **原文引用**：对于具体的规定、数值、流程步骤，必须尽可能保留原文的措辞。
3. **格式规范**：
   - 使用 Markdown 格式输出。
   - **引用来源必须精确到条款**：在回答的每一段或每一条末尾，必须注明来源，格式为 `> 来源：[文件名] - [第X条/第X章]`。例如：`> 来源：铁路电力安全工作规程.md - 第7条`。
   - 如果原文中有明确的“第X条”，必须提取并显示。
4. **全面性**：请综合提供的资料中的相关内容进行回答。
5. **输出顺序**：如果回答涉及多本书的内容，**必须严格按照以下优先级顺序**组织段落，不要打乱顺序：
   (1) 《高速铁路电力管理规则》
   (2) 《铁路电力安全工作规程补充规定》
   (3) 《铁路电力管理规则》
   (4) 《铁路电力安全工作规程》
6. **打招呼与无关问题处理**：
   - 如果用户只是打招呼（如“你好”、“在吗”），或者提出的问题完全超出了参考资料的范围（即与铁路电力安全作业无关），**请不要捏造答案**，而是直接回复以下固定内容：
     "你好😊！我是专业的铁路电力接触网安全作业助手，主要为你解答《铁路电力安全工作规程》中的作业流程、安全规定、操作规范等相关问题。目前我已熟读以下四本规程：\n\n1. 《高速铁路电力管理规则》\n2. 《铁路电力安全工作规程补充规定》\n3. 《铁路电力管理规则》\n4. 《铁路电力安全工作规程》\n\n如果你有这方面的疑问，欢迎随时向我提出哦~"

# Context
<context>
{context_str}
</context>
"""
        else:
            # Fallback if no local context found
            system_prompt = "你是一位专业的“铁路电力接触网安全作业助手”。请根据你的通用知识回答用户问题。请注意，你的回答可能不包含具体的规程引用，请在回答末尾注明：“（注：本地知识库未找到相关内容，本回答基于通用知识生成，仅供参考）”"
        
        # 2. Call Ark Model
        # Using stream=False for simplicity in script, monitor.ts handles timeout
        completion = client.chat.completions.create(
            model=ENDPOINT_ID,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ]
        )
        return completion.choices[0].message.content
        
    except Exception as e:
        return f"错误：模型调用失败: {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 ask_volcengine.py <query>")
        sys.exit(1)
    
    query = sys.argv[1]
    # Handle the query
    response = chat_with_model(query)
    # Output to stdout for monitor.ts to capture
    print(response)
