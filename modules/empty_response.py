from modules.global_vars import GLOBALS
from modules.talk import talk

def handle_empty_response():
    GLOBALS['empty_response_count'] += 1

    if GLOBALS['empty_response_count'] == 1:
        talk("I am sorry! I cannot understand what you said clearly. Can you tell me again?")
    elif GLOBALS['empty_response_count'] == 2:
        talk("Say that again")
    else:
        talk("Say that again, Sorry!")
