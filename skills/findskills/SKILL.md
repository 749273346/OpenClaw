# Find Skills (Discover Capabilities)

## Description
This skill allows the agent to inspect its own environment and list all available skills and extensions.
It scans the `/root/.openclaw/workspace/skills` and `/root/.openclaw/extensions` directories.

## When to use
- Use this skill when you need to know what capabilities are available.
- Use this skill to check if a specific skill or extension is installed.
- Use this skill to debug or verify the presence of new skills.

## Parameters
None.

## Returns
A JSON list of skills and extensions, including their names, types, paths, and descriptions.

## Usage
Execute the Python script:
```bash
python3 /root/.openclaw/workspace/skills/findskills/find_skills.py
```
