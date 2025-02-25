import speech_recognition as sr
from gtts import gTTS
from pygame import mixer
from googletrans import Translator
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import time
import os

# Load the GPT-2 model and tokenizer
model_name = "gpt2"  # You can also use "EleutherAI/gpt-neo-125M" for GPT-Neo
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# Set pad_token_id to eos_token_id for GPT-2
tokenizer.pad_token_id = tokenizer.eos_token_id

# Move the model to GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

# Initialize the translator
translator = Translator()

# Function to listen to the user's speech and convert it to text
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language="my-MM")  # my-MM for Burmese
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            print("Sorry, the service is down.")
            return None

# Function to speak the response
def speak(text, lang="my"):  # my for Burmese
    # Generate a unique filename using a timestamp
    filename = f"response_{int(time.time())}.mp3"
    
    try:
        # Convert text to speech and save as an MP3 file
        tts = gTTS(text=text, lang=lang)
        tts.save(filename)
        
        # Initialize pygame mixer
        mixer.init()
        mixer.music.load(filename)
        mixer.music.play()
        
        # Wait for the audio to finish playing
        while mixer.music.get_busy():
            continue
    finally:
        # Stop the mixer and release the file
        mixer.music.stop()
        mixer.quit()
        
        # Delete the file after playback
        try:
            os.remove(filename)
        except PermissionError:
            print(f"Warning: Could not delete {filename}. It may still be in use.")

# Function to translate text
def translate(text, src="my", dest="en"):
    try:
        translation = translator.translate(text, src=src, dest=dest)
        return translation.text
    except Exception as e:
        print(f"Translation error: {e}")
        return None

# Function to generate dynamic responses using Hugging Face Transformers
def generate_response(input_text):
    try:
        # Tokenize the input text and move to GPU
        inputs = tokenizer.encode(input_text, return_tensors="pt").to(device)
        
        # Generate a response with improved parameters
        outputs = model.generate(
            inputs,
            max_length=150,  # Maximum length of the response
            num_return_sequences=1,  # Number of responses to generate
            no_repeat_ngram_size=2,  # Avoid repeating phrases
            top_k=50,  # Limit the sampling pool
            top_p=0.95,  # Nucleus sampling
            temperature=0.9,  # Controls randomness
            do_sample=True,  # Enable sampling
            pad_token_id=tokenizer.pad_token_id,  # Use the set pad_token_id
            attention_mask=inputs.ne(tokenizer.pad_token_id).to(device),  # Set attention mask
        )
        
        # Decode the generated text
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Sorry, I couldn't generate a response at the moment."

# Main function to run the assistant
def main():
    while True:
        # Step 1: Listen to the user in Burmese
        user_input = listen()
        if user_input:
            # Step 2: Translate the input to English (optional)
            english_input = translate(user_input, src="my", dest="en")
            if not english_input:
                continue  # Skip if translation fails
            print(f"Translated Input: {english_input}")
            
            # Step 3: Generate a response using Hugging Face Transformers
            response = generate_response(english_input)  # Use Hugging Face for dynamic responses
            print(f"Generated Response: {response}")
            
            # Step 4: Translate the response back to Burmese
            burmese_response = translate(response, src="en", dest="my")
            if not burmese_response:
                continue  # Skip if translation fails
            print(f"AI: {burmese_response}")
            
            # Step 5: Speak the response in Burmese
            speak(burmese_response, lang="my")

if __name__ == "__main__":
    main()