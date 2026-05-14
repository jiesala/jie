import requests
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

GITHUB_MODELS_URL="https://models.inference.ai.azure.com"
# GITHUB_MODELS_URL = "https://models.github.ai/chat/completions"
GITHUB_TOKEN='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'




# For GitHub models
client = ChatCompletionsClient(
    endpoint=GITHUB_MODELS_URL,
    credential=AzureKeyCredential(GITHUB_TOKEN  ),
    model="DeepSeek-V3-0324" # Update as needed. Alternatively, you can include this is the `complete` call.
)



async def get_github_ai(user_question: str,context: str):
    try:
        response = client.complete(
            messages=[
                # SystemMessage("You are a helpful assistant."),
                UserMessage(f"{context}\n\n用户提问：{user_question}"),
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"api出错：{e}"


# async def get_github_ai(user_question: str,context: str):
#     headers={
#         "Authorization": f"Bearer {GITHUB_TOKEN}",
#         "Content-Type": "application/json"
#     }
#
#     payload={
#         "model":"DeepSeek-V3-0324",
#         "messages":[{"role":"user","content":f"{context}\n\n用户提问：{user_question}"}],
#         "temperature":0.4,
#         "stream":False
#     }
#
#     try:
#         response = requests.post(GITHUB_MODELS_URL, json=payload, headers=headers)
#         response.raise_for_status()
#         result = response.json()
#         return result["choices"][0]["message"]["content"]
#     except requests.exceptions.HTTPError as err:
#         return f"api出错：{err}"
