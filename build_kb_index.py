
import os
import json
import re
import pickle
import numpy as np
from zhipuai import ZhipuAI
from rank_bm25 import BM25Okapi
import jieba

# Configuration
KB_DIR = "/root/.openclaw/知识库资料"
INDEX_FILE = "/root/.openclaw/kb_index.pkl"
ZHIPU_API_KEY = "8160d175a76d4780bdd28cfa9a6324a2.PKy7AzPDMtROEBIV"

def get_chunks(kb_dir):
    chunks = []
    
    for filename in os.listdir(kb_dir):
        if not filename.endswith(".md"):
            continue
            
        filepath = os.path.join(kb_dir, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Split by headers (H1, H2, H3)
            # This regex splits by lines starting with #, capturing the header level and title
            # but keeping the delimiter
            # Actually, let's use a simpler approach: iterate lines and group by header
            lines = content.split('\n')
            current_chunk = []
            current_header = "Intro"
            
            for line in lines:
                if line.strip().startswith('#'):
                    if current_chunk:
                        chunk_text = "\n".join(current_chunk).strip()
                        if chunk_text:
                            chunks.append({
                                "filename": filename,
                                "header": current_header,
                                "content": chunk_text
                            })
                        current_chunk = []
                    current_header = line.strip()
                    current_chunk.append(line)
                else:
                    current_chunk.append(line)
            
            # Add last chunk
            if current_chunk:
                chunk_text = "\n".join(current_chunk).strip()
                if chunk_text:
                    chunks.append({
                        "filename": filename,
                        "header": current_header,
                        "content": chunk_text
                    })
                    
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            
    return chunks

def generate_embeddings(chunks):
    client = ZhipuAI(api_key=ZHIPU_API_KEY)
    embeddings = []
    
    print(f"Generating embeddings for {len(chunks)} chunks...")
    
    # Process one by one to avoid Request Entity Too Large and handle errors gracefully
    for i, chunk in enumerate(chunks):
        text = f"{chunk['filename']} {chunk['header']}\n{chunk['content']}"
        
        # Check length before sending
        if len(text) > 4000:
            print(f"[WARN] Chunk {i} from {chunk['filename']} is too long ({len(text)} chars). Truncating to 4000.")
            text = text[:4000]
            
        try:
            response = client.embeddings.create(
                model="embedding-3", 
                input=text
            )
            embedding = response.data[0].embedding
            embeddings.append(embedding)
            if i % 10 == 0:
                print(f"Processed {i}/{len(chunks)}")
        except Exception as e:
            print(f"Error generating embedding for chunk {i} ({chunk['filename']}, len={len(text)}): {e}")
            # Fallback to zero vector (dimension 2048 for embedding-3)
            embeddings.append([0.0] * 2048)

    return np.array(embeddings)

def build_bm25(chunks):
    # Tokenize content for BM25
    tokenized_corpus = []
    for chunk in chunks:
        text = f"{chunk['filename']} {chunk['header']} {chunk['content']}"
        tokens = list(jieba.cut_for_search(text))
        tokenized_corpus.append(tokens)
        
    bm25 = BM25Okapi(tokenized_corpus)
    return bm25

def main():
    print("Scanning Knowledge Base...")
    chunks = get_chunks(KB_DIR)
    print(f"Found {len(chunks)} chunks.")
    
    print("Building BM25 Index...")
    bm25 = build_bm25(chunks)
    
    print("Generating Embeddings...")
    embeddings = generate_embeddings(chunks)
    
    print("Saving Index...")
    index_data = {
        "chunks": chunks,
        "embeddings": embeddings,
        "bm25": bm25
    }
    
    with open(INDEX_FILE, 'wb') as f:
        pickle.dump(index_data, f)
        
    print(f"Index saved to {INDEX_FILE}")

if __name__ == "__main__":
    main()
