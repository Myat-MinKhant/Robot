import requests
import json
from googletrans import Translator


translator = Translator()

def translate_text(text):
  return translator.translate(text, dest='my').text


response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": "Bearer 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",
  },
  data=json.dumps({
    "model": "openai/gpt-3.5-turbo",
    "messages": [
      {
        "role": "user",
        "content": "what is ai"
      }
    ]
  })
)

response_data = response.json()

if "choices" in response_data and response_data["choices"]:
    answer = response_data["choices"][0]["message"]["content"]
    print(answer)
else:
    print("Unexpected response structure:", response_data)