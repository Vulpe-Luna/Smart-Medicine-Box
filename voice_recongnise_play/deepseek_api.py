import requests
import json

API_KEY = "sk-73b97dbb40ec4d0d83c5357a4802e301"

def ask_pillbox(question):
    print(f"[*] Sending to DeepSeek: '{question}'")
    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "system", 
                "content": "You are a helpful medical assistant for seniors. Keep your answers warm, professional, clear, and strictly under 50 words."
            },
            {"role": "user", "content": question}
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        answer = response.json()['choices'][0]['message']['content']
        return answer
    except Exception as e:
        print(f"[-] DeepSeek API Error: {e}")
        return "Sorry, the AI doctor network is currently unavailable."
