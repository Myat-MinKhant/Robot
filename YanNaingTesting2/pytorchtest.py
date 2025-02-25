import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load the GPT-2 model and tokenizer
model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# Move the model to GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

# Function to generate dynamic responses
def generate_response(input_text):
    # Tokenize the input text
    inputs = tokenizer.encode(input_text, return_tensors="pt").to(device)
    
    # Generate a response with improved parameters
    outputs = model.generate(
        inputs,
        max_length=100,  # Maximum length of the response
        num_return_sequences=1,  # Number of responses to generate
        no_repeat_ngram_size=2,  # Avoid repeating phrases
        top_k=50,  # Limit the sampling pool
        top_p=0.95,  # Nucleus sampling
        temperature=0.7,  # Controls randomness
        do_sample=True,  # Enable sampling
        pad_token_id=tokenizer.eos_token_id,  # Set pad token to EOS token
    )
    
    # Decode the generated text
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

# Test the function
input_text = "Tell me about myanmar"
response = generate_response(input_text)
print(response)