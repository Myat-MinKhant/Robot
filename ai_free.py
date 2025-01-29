from transformers import pipeline

def get_huggingface_response(prompt, model="gpt2"):
    try:
        generator = pipeline("text-generation", model=model)
        response = generator(prompt, max_length=50, num_return_sequences=1)
        return response[0]["generated_text"]
    except Exception as e:
        return f"Error with Hugging Face model: {e}"

prompt = "What is artificial intelligence?"
response = get_huggingface_response(prompt)
print(response)
