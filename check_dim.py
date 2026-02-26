
from zhipuai import ZhipuAI

ZHIPU_API_KEY = "8160d175a76d4780bdd28cfa9a6324a2.PKy7AzPDMtROEBIV"

try:
    client = ZhipuAI(api_key=ZHIPU_API_KEY)
    response = client.embeddings.create(
        model="embedding-3", 
        input="测试"
    )
    print(len(response.data[0].embedding))
except Exception as e:
    print(f"Error: {e}")
