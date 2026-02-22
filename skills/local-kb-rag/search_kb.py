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
    
    # Simple tokenization: split by spaces, also split by non-word chars if needed
    # For Chinese, maybe just split by spaces for now as user input is likely space-separated or full sentence
    # Better: simple unigram/bigram or just character matching for Chinese
    # Let's try splitting query into keywords
    query_terms = [t for t in query.split() if t]
    if not query_terms:
        # If no spaces, and looks like Chinese, maybe treat as single phrase
        # But also could be multiple words concatenated
        # For now, just use the whole query
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
                
                # Context snippet extraction
                # Find the first occurrence of the most significant term (or any term)
                # Prefer terms that appear in title first
                best_idx = -1
                for term in query_terms:
                    idx = content_lower.find(term.lower())
                    if idx != -1:
                        best_idx = idx
                        break
                
                if best_idx == -1: best_idx = 0
                
                start = max(0, best_idx - 50)
                end = min(len(content), best_idx + 450)
                snippet = content[start:end]
                if start > 0: snippet = "..." + snippet
                if end < len(content): snippet = snippet + "..."
                
                results.append({
                    'score': score,
                    'file': section['file'],
                    'path': path_str,
                    'content': snippet,
                    # 'full_content': content # Removed to reduce output size
                })
    
    # Sort by score descending
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:5] # Return top 5 matches

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 search_kb.py <query>")
        sys.exit(1)
    
    query = " ".join(sys.argv[1:])
    matches = search(query)
    
    if not matches:
        print("No matches found.")
    else:
        print(f"Found {len(matches)} matches for '{query}':\n")
        for i, match in enumerate(matches, 1):
            print(f"--- Match {i} ---")
            print(f"Source: {match['file']}")
            print(f"Location: {match['path']}")
            print(f"Content:\n{match['content'][:500]}...") # Limit content preview
            print("\n")
