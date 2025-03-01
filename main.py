import os
import openai
import threading
from dotenv import load_dotenv
from modules.run_ai import run_ai
from hardware.eyelids_servo import blink_eyes
from hardware.random_head_servo import random_movement
# from modules.wake_up import wake_word

def initialize_api():
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
initialize_api()

while True:
    # wake_word()
    # blink_thread = threading.Thread(target=blink_eyes, daemon=True)
    # random_move_thread = threading.Thread(target=random_movement, daemon=True)
    
    # blink_thread.start()
    # random_move_thread.start()

    run_ai()
