import os
import re

KB_DIR = "/root/.openclaw/知识库资料"

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    modified = False

    for line in lines:
        stripped = line.strip()
        # Check if line looks like a table separator
        if '|' in stripped and '---' in stripped:
            # Split by pipe
            parts = stripped.split('|')
            
            # Check if it's a valid table separator line
            # A valid separator line has at least one part that is just dashes/colons
            # and all non-empty parts must be dashes/colons
            
            is_separator = True
            valid_parts_count = 0
            
            clean_parts = []
            
            # Identify if the line starts/ends with pipe to handle empty first/last parts
            has_start_pipe = stripped.startswith('|')
            has_end_pipe = stripped.endswith('|')
            
            # We will process the parts that are actual columns
            # If split by |, ' | a | ' -> [' ', ' a ', ' ']
            # '| a |' -> ['', ' a ', '']
            
            # Let's iterate and check
            temp_parts = []
            
            # Determine range of parts to check
            start_idx = 1 if has_start_pipe else 0
            end_idx = len(parts) - 1 if has_end_pipe else len(parts)
            
            # If the split results in empty strings at ends because of pipes, ignore them for validation
            # but keep them for reconstruction? No, we reconstruct fully.
            
            # Actually, let's just look at the parts.
            # Any part that is NOT empty (whitespace) MUST match ^\s*:?-+:?\s*$
            
            cols = []
            for i, part in enumerate(parts):
                # Skip the implicit empty parts at start/end if they are empty
                if (i == 0 and part.strip() == '') or (i == len(parts)-1 and part.strip() == ''):
                    continue
                
                if part.strip() == '':
                    # Empty column? Valid in some markdown tables? 
                    # Usually separator line doesn't have empty columns unless it's malformed
                    is_separator = False
                    break
                
                if not re.match(r'^\s*:?-+:?\s*$', part):
                    is_separator = False
                    break
                
                cols.append(part)
            
            if is_separator and len(cols) > 0:
                # Reconstruct
                # Standard format: | :---: | :---: | ... |
                new_line = '|'
                for _ in cols:
                    new_line += ' :---: |'
                new_line += '\n'
                
                if new_line != line:
                    new_lines.append(new_line)
                    modified = True
                    print(f"[{os.path.basename(filepath)}] Fixed: {line.strip()} -> {new_line.strip()}")
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"Saved {filepath}")
    else:
        print(f"No changes for {filepath}")

def main():
    if not os.path.exists(KB_DIR):
        print(f"Directory not found: {KB_DIR}")
        return

    for filename in os.listdir(KB_DIR):
        if filename.endswith(".md"):
            filepath = os.path.join(KB_DIR, filename)
            process_file(filepath)

if __name__ == "__main__":
    main()
