import speech_recognition as sr
from modules.global_vars import GLOBALS

listener = sr.Recognizer()

def take_command(): 
    global listener
    while True:
        with sr.Microphone(device_index=1) as source:

            print('\n' + GLOBALS['bot_name'] +' listening..')

            listener.adjust_for_ambient_noise(source, duration=0.2)
            voice = listener.listen(source)

        print(GLOBALS['bot_name'] +' not listening..\n')
        try:
            command = listener.recognize_google(voice)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            continue
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            continue
    
        command = command.lower()
        
        if command is not None:
            command = command.replace(f"{GLOBALS['bot_name']}", "")
            return command