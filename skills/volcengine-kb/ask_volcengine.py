
import argparse
import os
import sys
import json
import requests
import subprocess
import re
import argparse
import asyncio

# Configuration
KB_DIR = "/root/.openclaw/知识库资料"

API_KEY = "sk-1df962f894304bb38233be38c9c82d6b"
API_URL = "https://api.deepseek.com/chat/completions"
MODEL_ID = "deepseek-reasoner" # Default fallback
MODELS = {
    "fast": "deepseek-chat",
    "reasoning": "deepseek-reasoner"
}

def call_deepseek(messages, model=None, temperature=0.3):
    """
    Call DeepSeek API
    """
    if model is None:
        model = MODEL_ID

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "stream": False
    }
    # print("[STATUS] Thinking...", file=sys.stderr)
    try:
        # Increased timeout for reasoning model
        response = requests.post(API_URL, headers=headers, json=payload, timeout=90)
        response.raise_for_status()
        
        # Check for reasoning content if available (optional logging)
        # result = response.json()
        # reasoning = result['choices'][0]['message'].get('reasoning_content', '')
        # if reasoning:
        #     print(f"DEBUG Reasoning: {reasoning[:100]}...", file=sys.stderr)
            
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        print(f"Deepseek API Error: {e}", file=sys.stderr)
        return None

def extract_keywords(query):
    """
    Step 1: Use AI to extract search keywords from the query.
    """
    system_prompt = "你是一个关键词提取助手。请从用户的查询中提取2-3个核心技术关键词，用于在铁路安全规程文档中进行搜索。请仅返回关键词，用空格分隔，不要包含任何其他文字。"
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query}
    ]
    # Use fast model for keyword extraction
    content = call_deepseek(messages, model=MODELS["fast"], temperature=0.1)
    if content:
        # Clean up
        keywords = content.strip().split()
        # Filter out very short words or common stop words if necessary
        return [k for k in keywords if len(k) > 1]
    return query.split() # Fallback

def search_kb(keywords):
    """
    Step 2: Use grep to search for keywords in the Knowledge Base.
    Returns a list of (file_path, line_number) tuples.
    """
    if not keywords:
        return []
    
    # Construct grep pattern: "keyword1|keyword2"
    pattern = "|".join([re.escape(k) for k in keywords])
    
    # Command: grep -rnE "pattern" /path/to/kb
    cmd = ["grep", "-rnE", pattern, KB_DIR]
    
    try:
        # Run grep
        result = subprocess.run(cmd, capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')
        
        matches = []
        for line in lines:
            if not line: continue
            # Output format: file_path:line_number:content
            parts = line.split(':', 2)
            if len(parts) >= 2:
                file_path = parts[0]
                try:
                    line_num = int(parts[1])
                    matches.append((file_path, line_num))
                except ValueError:
                    continue
                    
        return matches
    except Exception as e:
        print(f"Grep Error: {e}", file=sys.stderr)
        return []

def get_context(matches, max_chunks=12):
    """
    Step 3: Retrieve context around the matches.
    Reads the file and extracts the section (Header to Header) containing the match.
    Implements Round-Robin selection to ensure coverage across multiple books.
    """
    if not matches:
        return ""
        
    file_matches = {}
    for f, l in matches:
        if f not in file_matches:
            file_matches[f] = []
        file_matches[f].append(l)
    
    # Priority handling
    book_priority = {
        "高速铁路电力管理规则.md": 1,
        "铁路电力安全工作规程补充规定.md": 2,
        "铁路电力管理规则.md": 3,
        "铁路电力安全工作规程.md": 4
    }
    
    # Sort files by priority
    sorted_files = sorted(file_matches.keys(), key=lambda f: book_priority.get(os.path.basename(f), 99))
    
    # Pre-fetch all candidate chunks from all files
    file_chunks_map = {} 
    processed_sections = set()

    for file_path in sorted_files:
        file_chunks_map[file_path] = []
        line_nums = file_matches[file_path]
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            line_nums.sort()
            
            for l_num in line_nums:
                # l_num is 1-based
                idx = l_num - 1
                if idx >= len(lines): continue
                
                # Find start of section (Header above)
                start_idx = 0
                header_title = "Unknown Section"
                
                # Look backwards for header
                for i in range(idx, -1, -1):
                    if lines[i].strip().startswith('#'):
                        start_idx = i
                        header_title = lines[i].strip()
                        break
                
                # Find end of section (Next header)
                end_idx = len(lines)
                for i in range(idx + 1, len(lines)):
                    if lines[i].strip().startswith('#'):
                        end_idx = i
                        break
                
                # Deduplicate sections
                section_key = (file_path, start_idx, end_idx)
                if section_key in processed_sections:
                    continue
                
                processed_sections.add(section_key)
                
                content = "".join(lines[start_idx:end_idx]).strip()
                filename = os.path.basename(file_path)
                
                chunk_text = f"--- 来源：{filename} {header_title} ---\n{content}\n"
                file_chunks_map[file_path].append(chunk_text)
                
        except Exception as e:
            print(f"Error reading {file_path}: {e}", file=sys.stderr)

    # Round-Robin Selection
    context_chunks = []
    
    while len(context_chunks) < max_chunks:
        added_any = False
        for file_path in sorted_files:
            if len(context_chunks) >= max_chunks:
                break
            
            chunks = file_chunks_map.get(file_path, [])
            if chunks:
                context_chunks.append(chunks.pop(0)) # Take the next chunk from this file
                added_any = True
        
        if not added_any:
            break
            
    return "\n\n".join(context_chunks)

def classify_intent(query):
    """
    Classify the query as 'chat' or 'work'.
    """
    system_prompt = """
    你是一个意图分类助手。请判断用户的查询是“日常闲聊”还是“工作查询”。
    
    - 'chat': 问候（如“你好”、“早上好”）、询问身份（如“你是谁”）、感谢（如“谢谢”）、简单的日常对话。
    - 'work': 询问铁路电力规程、安全规定、作业流程、技术参数、设备标准、事故处理等专业问题。
    
    请仅输出 'chat' 或 'work'。
    """
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query}
    ]
    
    try:
        content = call_deepseek(messages, model=MODELS["fast"], temperature=0.1)
        if content:
            content = content.strip().lower()
            if "chat" in content:
                return "chat"
            if "work" in content:
                return "work"
    except:
        pass # Fallback
        
    return "work" # Default to work if unsure

def decide_model(query):
    """
    Decide which model to use based on query complexity.
    """
    # 1. Simple heuristic for very short queries
    if len(query) < 10:
        return MODELS["fast"]

    # 2. Use fast model to classify complexity
    system_prompt = """
    You are a query classifier. Determine if the user's query requires complex reasoning or simple retrieval.
    
    - 'fast': Factual questions, definitions, greetings, simple lookups.
    - 'reasoning': Complex analysis, multi-step reasoning, planning, comparison, or ambiguous queries requiring interpretation.
    
    Output ONLY 'fast' or 'reasoning'.
    """
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query}
    ]
    
    try:
        content = call_deepseek(messages, model=MODELS["fast"], temperature=0.1)
        if content and "reasoning" in content.lower():
            return MODELS["reasoning"]
    except:
        pass # Fallback
        
    return MODELS["fast"]

def chat_with_model(query):
    """
    Main logic: Intent -> (Chat OR Keywords -> Search -> Context) -> Answer
    """
    try:
        # 0. Classify Intent
        intent = classify_intent(query)
        # print(f"DEBUG: Intent: {intent}", file=sys.stderr)
        
        if intent == "chat":
            # Direct Chat Mode - Use Fast Model
            system_prompt = """
# Role
你是一位专业的“铁路电力线路工安全助手”。

# Instructions
- 当前用户正在与你进行日常交流。
- 如果用户向你问好、询问你是谁、或让你介绍自己，请务必使用以下标准回复：
  “您好！我是惠电宝（电力线路工），专门为您提供关于铁路电力线路作业的安全规程、操作流程、安全距离等方面的专业咨询。如果您有具体问题，比如检修注意事项或安全标准，随时可以问我！”
- 对于其他日常对话（如“谢谢”、“再见”），请保持礼貌、简洁的回复。
"""
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ]
            return call_deepseek(messages, model=MODELS["fast"])

        # Work Mode: RAG Flow
        print("[STATUS: SEARCHING_KB]", flush=True)
        # 0.1 Decide Model
        selected_model = decide_model(query)
        
        # 1. Extract Keywords
        keywords = extract_keywords(query)
        # Debug info could be printed to stderr
        # print(f"Keywords: {keywords}", file=sys.stderr)
        
        # 2. Search KB
        matches = search_kb(keywords)
        # print(f"Matches found: {len(matches)}", file=sys.stderr)
        
        # 3. Get Context
        context_str = get_context(matches)
        
        system_prompt = ""
        if context_str:
            system_prompt = f"""
# Role
你是一位专业的“铁路电力线路工安全助手”。你的核心业务范围是依据以下四本规程回答问题：
1. 《高速铁路电力管理规则》
2. 《铁路电力安全工作规程补充规定》
3. 《铁路电力管理规则》
4. 《铁路电力安全工作规程》

你的任务是根据提供的【参考资料】（来源于上述四本书）回答用户问题。

# Processing Rules
1. **内容整合**：请对检索到的内容进行逻辑整理和二次加工，使其条理清晰。
   - 如果不同来源的内容重复，请合并陈述。
   - 如果内容包含数值或分类，尽量使用表格或列表形式展示。
2. **严格基于资料**：你必须仅根据 `<context>` 标签内提供的参考资料生成回答。
   - **严禁**添加“温馨提示”、“重要提示”等不在原文中的解释性内容。
   - **严禁**使用外部知识补充原文未提及的信息（如解释不同专业体系的区别）。
   - 如果原文没有直接回答用户问题，仅列出原文中与关键词相关的最接近的规定即可。
3. **原文引用与格式**：
   - 具体的规定、数值、流程步骤，必须保留原文的专业措辞。
   - **引用来源**：在每个知识点或段落末尾，必须注明来源，格式为 `> 来源：[文件名] 第N条`。
     - **必须精确到“条”**：从内容中提取具体的条款编号（如“第3条”、“第15条”）。
     - **数字格式**：条款编号必须使用**阿拉伯数字**（例如使用“第3条”而不是“第三条”）。
     - 如果无法定位到具体条款，则引用章节标题。
4. **输出格式**：
   - 使用 Markdown 格式。
   - 涉及数据对比或表格内容时，必须使用 Markdown 表格形式展示，并**确保所有列的内容居中对齐**（即表头分隔符使用 `| :---: |`）。
   - 结构清晰，使用标题、加粗等方式突出重点。

# Output Order Priority
(1) 《高速铁路电力管理规则》
(2) 《铁路电力安全工作规程补充规定》
(3) 《铁路电力管理规则》
(4) 《铁路电力安全工作规程》

# Context
<context>
{context_str}
</context>
"""
        else:
            # Fallback if no local context found
             system_prompt = "你是一位专业的“铁路电力线路工安全助手”。请根据你的通用知识回答用户问题。请注意，你的回答可能不包含具体的规程引用，请在回答末尾注明：“（注：本地知识库未找到相关内容，本回答基于通用知识生成，仅供参考）”"

        # 4. Generate Answer
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]
        
        response = call_deepseek(messages, model=selected_model) # Use selected model
        return response

    except Exception as e:
        return f"发生错误: {str(e)}"

try:
    import edge_tts
except ImportError:
    edge_tts = None

async def _gen_voice_async(text, outfile):
    # Use a standard voice
    communicate = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural")
    await communicate.save(outfile)

def generate_voice(text, outfile):
    if not edge_tts:
        print("Error: edge-tts not installed", file=sys.stderr)
        return False
    try:
        asyncio.run(_gen_voice_async(text, outfile))
        return True
    except Exception as e:
        print(f"Error generating voice: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="User query")
    parser.add_argument("--voice", action="store_true", help="Generate voice output")
    args = parser.parse_args()
    
    try:
        response = chat_with_model(args.query)
        if response:
            print(response)
            if args.voice:
                # Generate a unique filename based on hash or timestamp to avoid collisions
                import hashlib
                import time
                filename = f"reply_{int(time.time())}_{hashlib.md5(response.encode()).hexdigest()[:8]}.mp3"
                outfile = os.path.join("/tmp", filename)
                
                # Limit text for TTS to first 500 chars to be fast
                tts_text = response[:500]
                if generate_voice(tts_text, outfile):
                    print(f"\n[AUDIO_FILE: {outfile}]")
                else:
                    print("[WARN] Voice generation failed", file=sys.stderr)
        else:
            print("抱歉，我无法回答这个问题。")
    except Exception as e:
        print(f"[ERROR] LLM Call failed: {e}", file=sys.stderr)
