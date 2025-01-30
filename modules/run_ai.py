from modules.global_vars import GLOBALS
from modules.file_manager import load_conversation, setup_directories
from modules.camera import open_camera
from modules.talk import talk
from modules.handle_input import handle_user_input
from dialogs.small_funcs import goodbye
from dialogs.handle_dialog import handle_custom_dialog
import threading


def run_ai():
    setup_directories()

    conversation_for_guest = []  # Separate conversation list for guests
    
    # Add system message for guests
    if GLOBALS["current_face"] is None or GLOBALS["current_face"] == 'Unknown':
        conversation_for_guest.append(f"{GLOBALS['system_persona']['role']}: {GLOBALS['system_persona']['content']}")
        
    # Start camera thread
    camera_thread = threading.Thread(target=open_camera)
    GLOBALS["streaming"] = True
    camera_thread.start()

    # # Specify the delay in minutes before deleting the files
    # deletion_delay_minutes = 30
    # deletion_complete = threading.Event()

    # # Start the file deletion thread
    # deletion_thread = threading.Thread(target=delete_files_after_delay, args=(deletion_delay_minutes, deletion_complete))
    # deletion_thread.start()
    
    while True:
        if GLOBALS["current_task"] != 'face_recognition':
            while not GLOBALS["task_completed"]:
                pass

        current_user_name = GLOBALS["current_face"] if GLOBALS["current_face"] not in [None, 'Unknown'] else "Guest"
        
        print(current_user_name)
        print('listening...')
        print(conversation_for_guest)
        GLOBALS["conversation"] = [conv_item.strip() for conv_item in GLOBALS["conversation"]]
        print(GLOBALS["conversation"])
          
        user_input = input("Ask: ") + '.'  # Simplified user input handling
        # user_input = take_command() + '.'
        print(user_input)
            
        if any(user_input in conv_item for conv_item in GLOBALS["conversation"]) and user_input == " hello":
            talk("Hello again")
            GLOBALS["current_task"] = 'face_recognition'
            GLOBALS["previous_task"] = 'face_recognition'
            continue
        # elif all(words in user_input for words in ["my", "name", "is"]):
        #     user_name = user_input.split("is")[-1].strip()
        #     user_name = user_name.replace(".", "")
        #     update_user_name(user_name)
        #     talk(respond_to_name(user_name))
        #     GLOBALS["conversation"] = load_conversation(current_user_name)
        #     continue
        elif any(keyword in user_input for keyword in ['do you see']):
            articles = ['a', 'an', 'the']
            if any(keyword in user_input for keyword in articles):
                GLOBALS["user_requested_object"] = user_input.split(f'{articles} ')[-1].strip().lower().replace('.', '')
            else:
                GLOBALS["user_requested_object"] = user_input.split('see ')[-1].strip().lower().replace('.', '')
            GLOBALS["current_task"] = 'object_detection'
            GLOBALS["task_changed"] = True
            GLOBALS["previous_task"] = GLOBALS["current_task"]
        elif 'what is this' in user_input or all(keyword in user_input for keyword in ['what', 'in my hand', 'hold']):
            GLOBALS["current_task"] = 'object_detection'
            GLOBALS["task_changed"] = True
            GLOBALS["previous_task"] = GLOBALS["current_task"]
        elif 'what is the color of this' in user_input:
            GLOBALS["user_requested_object"] = user_input.split('color of this')[-1].strip().lower().replace('.', '')
            GLOBALS["current_task"] = 'color_recognition'
            GLOBALS["task_changed"] = True
            GLOBALS["previous_task"] = GLOBALS["current_task"]
        elif 'what is the color' in user_input:
            GLOBALS["current_task"] = 'color_recognition'
            GLOBALS["task_changed"] = True
            GLOBALS["previous_task"] = GLOBALS["current_task"]
        elif 'how many finger' in user_input:
            GLOBALS['current_task'] = 'hand_tracking'
            GLOBALS['task_changed'] = True
            GLOBALS['previous_task'] = GLOBALS['current_task'] 
        elif any(keyword in user_input for keyword in ['now']):
            GLOBALS["current_task"] = GLOBALS["previous_task"]
            GLOBALS["task_changed"] = True
        elif handle_custom_dialog(user_input):
            GLOBALS["context"]["topic"] = None
            GLOBALS["current_task"] = 'face_recognition'
            GLOBALS["previous_task"] = 'face_recognition'
            continue
        elif any(keyword in user_input for keyword in ["bye", "good bye", "goodbye", "exit", "see you later", "se ya later"]):
            talk(goodbye())
            break
        else:
            handle_user_input(
                user_input,
                conversation_for_guest if current_user_name == "Guest" else GLOBALS["conversation"],
                current_user_name
            )
            GLOBALS["current_task"] = 'face_recognition'
            GLOBALS["previous_task"] = 'face_recognition'