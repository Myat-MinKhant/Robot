import requests
import json
from googletrans import Translator
from gtts import gTTS

API_KEY = "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"  # Replace with a new API key (don't share it!)
translator = Translator()

def translate_text(text, target_language):
    return translator.translate(text, dest=target_language).text


def get_openai_response(prompt):
    """Get AI response from OpenRouter API."""
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            data=json.dumps({
                "model": "openai/gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}]
            })
        )

        # Convert response to JSON
        response_data = response.json()

        # Check if response is valid
        if "choices" in response_data and response_data["choices"]:
            return response_data["choices"][0]["message"]["content"].strip()
        else:
            return "Error: AI response failed"
    except Exception as e:
        return f"Error in AI response: {str(e)}"

def main():
    try:
        text = input("Enter your question in Burmese: ")
        english_text = translate_text(text, "en")
        ai_response = get_openai_response(english_text)
        burmese_response = translate_text(ai_response, "my")
        if burmese_response:
            with open("burmese_response.txt", "w", encoding="utf-8") as file:
                file.write(burmese_response)

    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    main()
