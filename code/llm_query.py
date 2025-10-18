from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

debug = bool(int(os.getenv("DEBUG", "0")))
print("Debug mode:", debug)
if debug:
    api_key = "lm-studio"
    base_url = os.getenv("LMSTUDIO_BASE_URL", "pippo")
    model = os.getenv("DEBUG_MODEL", "pippo")
    # does not do anything really.
else:
    api_key = os.getenv("OPENROUTER_API_KEY")
    base_url = "https://openrouter.ai/api/v1"
    model = "openai/gpt-4o"

print(base_url)
client = OpenAI(
    api_key=api_key,
    base_url=base_url,
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
    if not debug:    
        response = client.chat.completions.create(
            model=model,
                messages=message
        )
        formatted_response = response.choices[0].message.content 
    else:
        formatted_response = "pippopippou debug"
    return formatted_response 
