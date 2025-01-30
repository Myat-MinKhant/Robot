# import pywhatkit
# import wikipedia
import os
import openai
from dotenv import load_dotenv
from modules.run_ai import run_ai
from modules.wake_up import wake_word

def initialize_api():
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
initialize_api()

while True:
    # wake_word()
    run_ai()
    

    
    

    
