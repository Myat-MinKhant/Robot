from modules.global_vars import GLOBALS
from modules.file_manager import setup_directories, save_conversation
from modules.camera import open_camera
from modules.talk import talk
from modules.handle_input import handle_user_input
from dialogs.small_funcs import goodbye
from dialogs.handle_dialog import handle_custom_dialog
from utilities.pdf_load_text import load_text
from modules.preprocess import get_pdf_response, preprocess_response
import threading
from utilities.languages_detection import detect_language
from utilities.languages_translation import translate

def run_ai():
    setup_directories()
    pdf_text = load_text("/home/pi/Desktop/Robot/resources/pdf_files/ameca.text")

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
          
        original_userinput = input("Ask: ")  # Simplified user input handling
        # user_input = take_command() + '.'
        
        if original_userinput:
            GLOBALS['detected_language'] = detect_language(original_userinput)
            print(GLOBALS['detected_language'])

            print('translating to english...')

            user_input = translate(original_userinput, 'mya_Mymr', 'eng_Latn') if GLOBALS['detected_language'] == 'mya_Mymr' else original_userinput

            # user_input = user_input[0]['translation_text'] if GLOBALS['detected_language'] == 'mya_Mymr' else original_userinput

            user_input = user_input.lower().replace('?', '').replace('amora', '') + '.'
 
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
            elif 'what is this.' in user_input or 'what is it.' in user_input or all(keyword in user_input for keyword in ['what', 'in my hand', 'hold']):
                GLOBALS["current_task"] = 'object_detection'
                GLOBALS["task_changed"] = True
                GLOBALS["previous_task"] = GLOBALS["current_task"]
            elif 'what is the color of this' in user_input:
                GLOBALS["user_requested_object"] = user_input.split('color of this')[-1].strip().lower().replace('.', '')
                GLOBALS["current_task"] = 'color_recognition'
                GLOBALS["task_changed"] = True
                GLOBALS["previous_task"] = GLOBALS["current_task"]
            elif 'what is the color.' in user_input or 'what color is it' in user_input:
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
            elif pdf_text:
                response = get_pdf_response(user_input, pdf_text)
                response = response.lower().strip('.')
                if response == 'no_info' or response == 'no info':
                # if response  in any["no_info", "no info"]:
                    handle_user_input(
                        user_input,
                        conversation_for_guest if current_user_name == "Guest" else GLOBALS["conversation"],
                        current_user_name
                    )
                    GLOBALS["current_task"] = 'face_recognition'
                    GLOBALS["previous_task"] = 'face_recognition'
                else:
                    talk(response)
                    if current_user_name:
                        preprocess_response(response)
                        GLOBALS['conversation'].append(f"{current_user_name}: {user_input}")
                        GLOBALS['conversation'].append(f"{GLOBALS['bot_name']}: {response}")
                        save_conversation(current_user_name, GLOBALS['conversation'])

                    GLOBALS["context"]["topic"] = None
                    GLOBALS["current_task"] = 'face_recognition'
                    GLOBALS["previous_task"] = 'face_recognition'
                continue
            if any(keyword in user_input for keyword in ["bye", "good bye", "goodbye", "exit", "see you later", "se ya later"]):
                talk(goodbye())
                break

            