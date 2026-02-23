import os
import json
import sys

WORKSPACE_SKILLS_DIR = "/root/.openclaw/workspace/skills"
EXTENSIONS_DIR = "/root/.openclaw/extensions"

def find_skills():
    skills = []
    
    # Scan workspace skills
    if os.path.exists(WORKSPACE_SKILLS_DIR):
        for name in os.listdir(WORKSPACE_SKILLS_DIR):
            path = os.path.join(WORKSPACE_SKILLS_DIR, name)
            if os.path.isdir(path):
                skill_info = {
                    "name": name,
                    "type": "workspace_skill",
                    "path": path
                }
                # Try to read description from SKILL.md
                skill_md = os.path.join(path, "SKILL.md")
                if os.path.exists(skill_md):
                    try:
                        with open(skill_md, "r", encoding="utf-8") as f:
                            # Read first few lines for description
                            lines = f.readlines()
                            description = ""
                            for line in lines:
                                if line.strip() and not line.startswith("#"):
                                    description = line.strip()
                                    break
                            skill_info["description"] = description
                    except Exception:
                        pass
                skills.append(skill_info)

    # Scan extensions
    if os.path.exists(EXTENSIONS_DIR):
        for name in os.listdir(EXTENSIONS_DIR):
            path = os.path.join(EXTENSIONS_DIR, name)
            if os.path.isdir(path):
                ext_info = {
                    "name": name,
                    "type": "extension",
                    "path": path
                }
                # Try to read package.json
                pkg_json = os.path.join(path, "package.json")
                if os.path.exists(pkg_json):
                    try:
                        with open(pkg_json, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            ext_info["description"] = data.get("description", "")
                            ext_info["version"] = data.get("version", "")
                    except Exception:
                        pass
                skills.append(ext_info)
    
    return skills

if __name__ == "__main__":
    try:
        result = find_skills()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}, indent=2, ensure_ascii=False))
        sys.exit(1)
