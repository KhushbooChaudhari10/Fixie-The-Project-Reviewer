import requests
import os
from services import extract_text_from_py_files
from dotenv import load_dotenv
load_dotenv()

model="deepseek-ai/DeepSeek-R1-0528:novita"
    
url = "https://router.huggingface.co/v1/chat/completions"

HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
headers = {
            "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"
 }
def ask_llama(prompt, all_text):
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Python File:\n{all_text}"},           
        ],
        "temperature": 0.2,
        "max_tokens": 3000  # Increased for longer output
        }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        result = response.json()
        print("✅ Raw HF API result:", result)

        message = result["choices"][0]["message"]
        # ✅ Try content first, fallback to reasoning_content
        return message.get("content") or message.get("reasoning_content") or "⚠️ No suggestions found in response."

    except Exception as e:
        print("❌ Hugging Face error:", e)
        return "❌ Failed to get suggestions from Fixie."