import os
import time
from modules.global_vars import GLOBALS

def setup_directories():
    os.makedirs(GLOBALS["CONVERSATIONS_FOLDER"], exist_ok=True)

def save_conversation(username, conversation):
    if username:
        setup_directories()
        filename = os.path.join(GLOBALS["CONVERSATIONS_FOLDER"], f"{username}.txt")

        if os.path.exists(filename):
            with open(filename, 'w') as file:
                file.write(f"{GLOBALS['system_persona']['role']}: {GLOBALS['system_persona']['content']}\n")
                user_input_found = False
                for line in conversation:
                    cleaned_line = line.strip()
                    if f"{username}:" in cleaned_line:
                        user_input_found = True
                    if user_input_found:
                        file.write(f"{cleaned_line}\n")
                        
            print(f"Conversation with {username} appended.")    
        else:
            # Create a new file for the current user
            with open(filename, 'w') as file:
                user_input_found = False
                file.write(f"{GLOBALS['system_persona']['role']}: {GLOBALS['system_persona']['content']}\n")
                for line in conversation:
                    cleaned_line = line.strip()
                    if f"{username}:" in cleaned_line:
                        user_input_found = True
                    if user_input_found:
                        file.write(f"{cleaned_line}\n")  
            print(f"Conversation with {username} saved.")
    else:
        pass

    
def load_conversation(username):
    filename = os.path.join(GLOBALS["CONVERSATIONS_FOLDER"], f"{username}.txt")
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return file.readlines()
    else:
        return []
    
def delete_files_after_delay(delay_minutes, deletion_complete):
    start_time = time.time()
    end_time = start_time + (delay_minutes * 60)
    
    while time.time() < end_time:
        time.sleep(1)

    try:
        for file_name in os.listdir(GLOBALS["CONVERSATIONS_FOLDER"]):
            if file_name.endswith(".txt"):
                file_path = os.path.join(GLOBALS["CONVERSATIONS_FOLDER"], file_name)
                os.remove(file_path)
                print(f"File '{file_path}' deleted successfully.")

        # Delete user_data_info.json in the root directory
        root_user_data_info = "resources/user_data_info.json"
        if os.path.exists(root_user_data_info):
            os.remove(root_user_data_info)
            print(f"File '{root_user_data_info}' deleted successfully.")
        deletion_complete.set()
    except OSError as e:
        print(f"Error deleting files: {e}")