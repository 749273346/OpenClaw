
import os
from volcenginesdkarkruntime import Ark

# 配置
API_KEY = "99073b82-9920-42ea-92d1-7b75a1e3f274"
ENDPOINT_ID = "ep-m-20260222201045-gvjbn"

def chat_with_ark():
    client = Ark(api_key=API_KEY)
    
    print("已连接到火山引擎 Ark 大模型 (Doubao-Seed-1.8)")
    print("输入 'exit' 退出对话\n")
    
    # 初始化对话历史，加入系统预设
    messages = [
        {
            "role": "system",
            "content": "你是一位专业的“铁路电力线路工安全作业助手”。你的任务是回答用户关于作业流程、安全规定、操作规范等问题。虽然你现在没有连接到实时知识库，但请尽你所能根据你的训练知识提供专业、严谨的回答。"
        }
    ]
    
    while True:
        try:
            user_input = input("\n用户: ")
            if user_input.lower() in ["exit", "quit", "退出"]:
                break
                
            messages.append({"role": "user", "content": user_input})
            
            print("助手: ", end="", flush=True)
            
            stream = client.chat.completions.create(
                model=ENDPOINT_ID,
                messages=messages,
                stream=True
            )
            
            full_response = ""
            for chunk in stream:
                if not chunk.choices:
                    continue
                content = chunk.choices[0].delta.content
                if content:
                    print(content, end="", flush=True)
                    full_response += content
            
            print() # 换行
            messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            print(f"\n发生错误: {e}")

if __name__ == "__main__":
    chat_with_ark()
