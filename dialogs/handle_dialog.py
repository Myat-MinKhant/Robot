from modules.global_vars import GLOBALS
from modules.file_manager import save_conversation, load_conversation
from modules.talk import talk
from dialogs.large_funcs import custom_dialog


def handle_custom_dialog(user_input):

    current_username = GLOBALS['current_face']
    response_string = custom_dialog(user_input)
    GLOBALS['conversation'] = load_conversation(current_username)

    if response_string: 
        print("Robot is thinking...")

        # Use talk to handle speech and servos together
        talk(response_string)

        # Handle contextual dialog based on the current topic
        if GLOBALS['dialog']:
            if GLOBALS['context'].get("topic") == 'ask_user_name':
                talk("What is your name?")
                GLOBALS['context']["topic"] = None
                GLOBALS['dialog'] = False
            elif GLOBALS['context'].get("topic") == 'asking_look':
                talk("Do you think I look good?")
                GLOBALS['context']["topic"] = None
                GLOBALS['dialog'] = False
            elif GLOBALS['context'].get("topic") == 'relations':
                talk("Do you have a boyfriend?", delay=2)
                talk("I'll take that as a yes.")
                GLOBALS['context']["topic"] = None
                GLOBALS['dialog'] = False
            elif GLOBALS['context'].get("topic") == 'joke':
                talk("Do you want to hear my favorite one?")
                GLOBALS['context']["topic"] = "joke"
                GLOBALS['dialog'] = False
            elif GLOBALS['context'].get("topic") == 'where_are_you_from':
                talk("Where are you from?")
                GLOBALS['context']["topic"] = None
                GLOBALS['dialog'] = False
            elif GLOBALS['context'].get("topic") == 'greeting':
                talk("How are you?")
                GLOBALS['context']["topic"] = None
                GLOBALS['dialog'] = False
                      
        if current_username:
            # Log the conversation
            GLOBALS['conversation'].append(f"{current_username}: {user_input}")
            GLOBALS['conversation'].append(f"{GLOBALS['bot_name']}: {response_string}")
            save_conversation(current_username, GLOBALS['conversation'])
        
        return True  # Custom dialog handled
    return False