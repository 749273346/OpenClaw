import os
import sys
import glob
import re

KB_DIR = "/root/.openclaw/知识库资料"

def parse_markdown(file_path):
    """
    Parses a markdown file into sections with hierarchy.
    Returns a list of dicts: {'file': filename, 'path': [h1, h2, ...], 'content': text}
    """
    sections = []
    current_path = []
    current_content = []
    
    filename = os.path.basename(file_path)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            match = re.match(r'^(#+)\s+(.*)', line)
            if match:
                # Save previous section
                if current_content:
                    sections.append({
                        'file': filename,
                        'path': list(current_path),
                        'content': '\n'.join(current_content)
                    })
                    current_content = []
                
                level = len(match.group(1))
                title = match.group(2).strip()
                
                # Update path based on level
                # If level is deeper than current, append
                # If level is same or higher, pop until correct depth
                # Headers: # (1), ## (2), ### (3)
                # If current_path has length 2 (H1, H2), and new header is H2 (level 2),
                # we should pop until length is 1, then append new H2.
                # If new header is H3 (level 3), append.
                # If new header is H1 (level 1), pop all.
                
                # Simple logic: truncate path to level-1
                current_path = current_path[:level-1]
                current_path.append(title)
                
            else:
                current_content.append(line)
        
        # Add last section
        if current_content:
            sections.append({
                'file': filename,
                'path': list(current_path),
                'content': '\n'.join(current_content)
            })
            
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        
    return sections

def search(query):
    results = []
    files = glob.glob(os.path.join(KB_DIR, "*.md"))
    
    # Pre-process query to handle natural language questions
    # Replace common Chinese particles/question words with spaces to create keywords
    clean_q = query
    for char in ["是什么", "有哪些", "怎么做", "的", "吗", "？", "?", "是", "哪些", "什么"]:
        clean_q = clean_q.replace(char, " ")
    
    # Split by spaces to get terms
    query_terms = [t for t in clean_q.split() if t]
    
    if not query_terms:
        # Fallback to original if everything was stripped (unlikely but possible)
        query_terms = [query]
            
    for file_path in files:
        sections = parse_markdown(file_path)
        for section in sections:
            content = section['content']
            path_str = ' > '.join(section['path']) if section['path'] else "Intro"
            
            # Scoring:
            # - Title match: heavy weight
            # - Content match: medium weight
            # - Exact phrase match: bonus
            
            score = 0
            
            # Check title/path matches
            path_lower = path_str.lower()
            content_lower = content.lower()
            
            term_scores = []
            for term in query_terms:
                term_lower = term.lower()
                term_score = 0
                
                # Title/Path match
                if term_lower in path_lower:
                    term_score += 10
                    
                # Content match
                count = content_lower.count(term_lower)
                if count > 0:
                    term_score += count
                
                term_scores.append(term_score)
            
            # Require at least one term match
            if sum(term_scores) > 0:
                score = sum(term_scores)
                
                # Bonus for exact phrase match in content
                if query.lower() in content_lower:
                    score += 20
                
                # Context snippet extraction - REMOVED to return full content as requested
                # The user wants the exact content verbatim, no summarization or truncation.
                
                results.append({
                    'score': score,
                    'file': section['file'],
                    'path': path_str,
                    'content': content, # Return FULL content
                })
    
    # Sort by score descending
    results.sort(key=lambda x: x['score'], reverse=True)
    
    # Format the output strictly as requested by the user
    # "回答之前告诉这是哪个文件哪一章的第几条，然后将结果原封不动的返回出来"
    final_output = []
    if not results:
        print(f"未找到关于 '{query}' 的相关内容。")
        return []

    # Only return the top 1 result to avoid overwhelming the user, or maybe top 3 if requested.
    # The user said "将结果原封不动的返回出来", implying specific answers.
    # Let's return the top match fully, and maybe mention others briefly if needed.
    # For now, let's return top 1 full content to ensure "verbatim" without hitting token limits too hard.
    # Actually, the user might want to see multiple if they are relevant.
    # Let's try returning top 1-2 matches with full content.
    
    final_output = []
    for i, res in enumerate(results[:1]): # Limit to top 1 for precision as requested
        output = f"【来源】：{res['file']} > {res['path']}\n【内容】：\n{res['content']}\n"
        final_output.append(output)
    
    print("\n".join(final_output))
    return results[:1]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 search_kb.py <query>")
        sys.exit(1)
    
    query = " ".join(sys.argv[1:])
    search(query)
