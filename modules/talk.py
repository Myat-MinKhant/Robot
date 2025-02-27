from modules.global_vars import GLOBALS
import threading
import time
import subprocess
from playsound import playsound
from gtts import gTTS
from utilities.languages_translation import translate
# from modules.lips_servo import generate_servo_movements, move_servos


def talk(text, delay=0):
    text = text.replace(f"{GLOBALS['bot_name']}: ", "").replace(f"{GLOBALS['current_face']}: ", "")
    
    if GLOBALS['detected_language'] == 'mya_Mymr':
        print('Translating response to Burmese...')
        translated_response = translate(text, 'eng_Latn', 'mya_Mymr')
        print(translated_response)
    else:
        print(text)
    
    GLOBALS['detected_language'] = 'eng_Latn'



    # # Generate servo movements before speaking
    # servo_movements = generate_servo_movements(text)

    # # Create threads for TTS and servo movement
    # talk_thread = threading.Thread(target=_speak_text, args=(text, delay))
    # servo_thread = threading.Thread(target=move_servos, args=(servo_movements,))

    # # Start both threads
    # talk_thread.start()
    # servo_thread.start()

    # # Wait for both threads to finish
    # talk_thread.join()
    # servo_thread.join()


def _speak_text(text, delay):
    subprocess.call(["espeak", "-s", "155", "-v", "en+f2", text])
    time.sleep(delay)

# def talk_japanese(text):
#     translated_text = translator.translate(text , dest='ja').text
#     # print(translated_text)
#     translation = gTTS(translated_text, lang='ja')
#     translation.save('voice.mp3')
#     talk(f"In japanese, it is")
#     playsound(".\\voice.mp3")


