import speech_recognition as sr
from gtts import gTTS
from pygame import mixer
from googletrans import Translator
import time
import os

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
    translation = translator.translate(text, src=src, dest=dest)
    return translation.text

# Function to generate dynamic responses
def generate_response(input_text):
    # Convert input to lowercase for easier matching
    input_text = input_text.lower()
    
    # Define rules for responses
    if "hello" in input_text or "hi" in input_text:
        return "Hello! How can I help you?"
    elif "how are you" in input_text:
        return "I am doing well, thank you!"
    elif "name" in input_text:
        return "My name is Burmese Assistant."
    elif "thank you" in input_text:
        return "You're welcome!"
    elif "what are you doing" in input_text:
        return "I am here to assist you."
    else:
        return "I'm sorry, I didn't understand that."

# Main function to run the assistant
def main():
    while True:
        # Step 1: Listen to the user in Burmese
        user_input = listen()
        if user_input:
            # Step 2: Translate the input to English (optional)
            english_input = translate(user_input, src="my", dest="en")
            print(f"Translated Input: {english_input}")
            
            # Step 3: Generate a response based on the input
            response = generate_response(english_input)  # Use the dynamic response function
            
            # Step 4: Translate the response back to Burmese
            burmese_response = translate(response, src="en", dest="my")
            print(f"AI: {burmese_response}")
            
            # Step 5: Speak the response in Burmese
            speak(burmese_response, lang="my")

if __name__ == "__main__":
    main()