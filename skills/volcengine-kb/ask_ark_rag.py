
import sys
from volcenginesdkarkruntime import Ark

# Configuration
API_KEY = "99073b82-9920-42ea-92d1-7b75a1e3f274"
ENDPOINT_ID = "ep-m-20260222201045-gvjbn"

def chat_with_ark_rag(query, context):
    client = Ark(api_key=API_KEY)
    
    system_prompt = f"""
# Role
你是一位专业的“铁路电力线路工安全作业助手”。你的唯一任务是根据提供的【参考资料】回答用户关于作业流程、安全规定、操作规范等问题。

# Constraints & Rules
1. **严格基于资料**：你必须仅根据 `<context>` 标签内提供的参考资料回答问题。严禁编造信息或使用你训练数据中的外部知识。
2. **拒绝无中生有**：如果参考资料中没有包含用户问题的答案，请直接回复：“知识库中未找到相关内容，请核实问题或查阅原始规程。”
3. **原文引用**：对于具体的规定、数值、流程步骤，必须尽可能保留原文的措辞，不要随意改写，以确保安全规程的严谨性。
4. **格式规范**：
   - 使用 Markdown 格式输出。
   - 涉及数据对比或表格内容时，必须使用 Markdown 表格形式展示。
   - 必须在回答末尾注明来源，格式为：`> 来源：[文件名] - [章节]`。
   - 涉及到步骤时，使用有序列表（1. 2. 3.）。
   - 涉及到并列项时，使用无序列表（- ）。
5. **语气风格**：专业、严谨、客观，不使用“根据提供的文档”、“参考资料显示”等冗余口语，直接陈述事实。

# Context
<context>
{context}
</context>
"""

    try:
        completion = client.chat.completions.create(
            model=ENDPOINT_ID,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ]
        )
        print(completion.choices[0].message.content)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 ask_ark_rag.py <query> <context>")
        sys.exit(1)
    
    query = sys.argv[1]
    context = sys.argv[2]
    chat_with_ark_rag(query, context)
