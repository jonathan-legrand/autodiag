from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

def call_api(prompt: list, role:str) -> dict:
    message = []
    for msg in prompt:
        if msg["role"] == role:
            message.append({"role": "assistant", "content": msg["content"]})
        elif msg["role"] == "system":
            message.append(msg)
        else:
            message.append({"role": "user", "content": msg["content"]})
        
    response = client.chat.completions.create(
        model="openai/gpt-4o",
            messages=message
    )
    formatted_response = response.choices[0].message.content 
    return formatted_response 
