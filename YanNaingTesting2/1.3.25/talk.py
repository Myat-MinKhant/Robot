# import sys
# import os

# # Add the 'modules' directory to the Python path
# # sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'modules'))
# sys.path.append(r"C:\Users\ASUS\Documents\AmecaRobot\Robot\modules")

# from modules.global_vars import GLOBALS
import sys
import os

# Get the absolute path of the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))



# Add it to sys.path
sys.path.append(project_root)

# Now import the module
from modules.global_vars import GLOBALS
from playsound import playsound
from utilities.languages_translation import translate
import requests
from pydub import AudioSegment
from pydub.playback import play
import asyncio
import random
import edge_tts
from edge_tts import VoicesManager

OUTPUT_PATH = "/home/pi/Desktop/Robot/voices/talk.mp3"

def talk(text, delay=0):
    text = text.replace(f"{GLOBALS['bot_name']}: ", "").replace(f"{GLOBALS['current_face']}: ", "")
    
    if GLOBALS['detected_language'] == 'mya_Mymr':
        print('Translating response to Burmese...')
        translated_response = translate(text, 'eng_Latn', 'mya_Mymr')

        # Convert English names to Burmese phonetics
        translated_response = convert_names_to_burmese(translated_response)

        asyncio.run(generate_tts(translated_response))
        print(translated_response)
    else:
        asyncio.run(generate_tts(text))
        print(text)

    GLOBALS['detected_language'] = 'eng_Latn'

async def generate_tts(translated_response, output_filename=OUTPUT_PATH, gender="Female", language="my"):
    voices = await VoicesManager.create()
    voice_list = voices.find(Gender=gender, Language=language)

    if not voice_list:
        print("❌ No voices found for the specified gender and language!")
        return

    selected_voice = random.choice(voice_list)["Name"]
    communicate = edge_tts.Communicate(translated_response, selected_voice)
    
    await communicate.save(output_filename)

    sound = AudioSegment.from_mp3('/home/pi/Desktop/Robot/voices/talk.mp3')
    play(sound)

# English-to-Burmese phonetic dictionary for common names
name_phonetic_dict = {
    "Nay Toe": "နေတိုး",
    "Paing Phyo Thu": "ပိုင်ဖြိုးသု",
    "Wutt Hmone Shwe Yi": "ဝတ်မှုန်ရွှေရည်",
    "Aung Ye Lin": "အောင်ရဲလင်း",
    "Phway Phway": "ဖွေးဖွေး",
    "Sai Sai Kham Leng": "စိုင်းစိုင်းခမ်းလှိုင်",
    "Thet Mon Myint": "သက်မွန်မြင့်",
    "Pyay Ti Oo": "ပြေတီဦး",
    "Eaindra Kyaw Zin": "အိန္ဒြာကျော်ဇင်",
    "Yan Aung": "ယံအောင်",
    "Tun Tun": "ထွန်းထွန်း",
    "Lu Min": "လူမင်း",
    "May Than Nu": "မေသန်းနု",
    "Khant Si Thu": "ခန့်စည်သူ",
    "Zenn Kyi": "ဇဏ်ခီ",
    "Aye Myat Thu": "အေးမြတ်သူ",
    "Daung": "ဒေါင်း",
    "Thinzar Wint Kyaw": "သင်ဇာဝင့်ကျော်",
    "Htun Eaindra Bo": "ထွန်းအိန္ဒြာဗို",
    "Soe Myat Thuzar": "စိုးမြတ်သူဇာ",
    "Kyaw Kyaw Bo": "ကျော်ကျော်ဗိုလ်",
    "Nay Min": "နေမင်း",
    "Phoe Chit": "ဖိုးချစ်",
    "Eaint Myat Chal": "အိမ့်မြတ်ခြယ်",
    "Moe Hay Ko": "မိုးဟေကို",
    "Nan Su Yati Soe": "နန်းဆုရတီစိုး",
    "Aung La Nsang": "အောင်လအန်ဆန်း",
    "Soe Pyae Thazin": "စိုးပြည့်သဇင်",
    "Khin Wint Wah": "ခင်ဝင့်ဝါ",
    "Ei Chaw Po": "အိချောပို",
    "Sung Tin Par": "ဆုန်သင်းပါ",
    "Okkar Min Maung": "ဥက္ကာမင်းမောင်",
    "Min Maw Kun": "မင်းမော်ကွန်း",
    "Aung Myint Myat": "အောင်မြင့်မြတ်",
    "Myint Myat": "မြင့်မြတ်",
    "Kyaw Htet Aung": "ကျော်ထက်အောင်",
    "Pyae Pyae": "ပြည့်ပြည့်",
    "Nine Nine": "နိုင်နိုင်း",
    "Wai Lu Kyaw": "၀ေလုကျော်",
    "Mo Mo Myint Aung": "မို့မို့မြင့်အောင်",
    "Nan Myat Phyo Thinn": "နန်းမြတ်ဖြိုးသင်း"
}

def convert_names_to_burmese(text):
    """Replace English names with their Burmese phonetic spellings."""
    for eng_name, burmese_name in name_phonetic_dict.items():
        text = text.replace(eng_name, burmese_name)
    return text