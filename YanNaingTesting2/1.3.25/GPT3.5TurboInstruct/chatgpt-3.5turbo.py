##Working as Expected!!

from openai import OpenAI
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# Initialize OpenAI client for OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",  # Replace with your API key
)

# Initialize the translation pipeline
checkpoint = "facebook/nllb-200-distilled-600M"
model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)
tokenizer = AutoTokenizer.from_pretrained(checkpoint)

# Translation function
def translate(text, src_lang="mya_Mymr", tgt_lang="eng_Latn"):
    try:
        translator = pipeline('translation', model=model, tokenizer=tokenizer, src_lang=src_lang, tgt_lang=tgt_lang, max_length=600, device=0)  # Use GPU
        output = translator(text)
        return output[0]["translation_text"]
    except Exception as e:
        print(f"Translation error: {str(e)}")
        return None

# Main chat loop
def chat():
    print("Chatbot is ready! Type 'exit' to quit.")
    
    while True:
        # Get user input
        user_input = input("You: ")
        
        if user_input.lower() == "exit":
            print("Exiting chat. Goodbye!")
            break

        # Translate Burmese input to English
        english_input = translate(user_input, src_lang="mya_Mymr", tgt_lang="eng_Latn")
        if not english_input:
            continue  # Skip if translation fails

        # Send the English input to GPT-3.5 Turbo Instruct via OpenRouter
        try:
            completion = client.chat.completions.create(
                extra_headers={},
                extra_body={},
                model="openai/gpt-3.5-turbo-instruct",  # Using GPT-3.5 Turbo Instruct
                messages=[{"role": "user", "content": english_input}]  # Send only the current message
            )

            # Get AI response in English
            english_response = completion.choices[0].message.content.strip()

            # Translate the AI's English response back to Burmese
            burmese_response = translate(english_response, src_lang="eng_Latn", tgt_lang="mya_Mymr")
            if not burmese_response:
                continue  # Skip if translation fails

            # Print AI response
            print(f"AI: {burmese_response}")
        except Exception as e:
            print(f"Error: Failed to get AI response: {str(e)}")

# Start the chat
if __name__ == "__main__":
    chat()