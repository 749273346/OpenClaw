
import os
from volcenginesdkarkruntime import Ark

client = Ark(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key="99073b82-9920-42ea-92d1-7b75a1e3f274"
)

print("Attributes of client.bot_chat:")
try:
    for attr in dir(client.bot_chat):
        if not attr.startswith("_"):
            print(attr)
except:
    print("Error inspecting client.bot_chat")

print("\nAttributes of client.bot_chat.completions:")
try:
    for attr in dir(client.bot_chat.completions):
        if not attr.startswith("_"):
            print(attr)
except:
    print("Error inspecting client.bot_chat.completions")
