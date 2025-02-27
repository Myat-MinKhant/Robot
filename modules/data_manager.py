import os
import json
from modules.global_vars import GLOBALS

DATA_FILE = "resources/user_data_info.json"
    
def save_user_info(user_info):
    with open (DATA_FILE, 'w') as file:
        json.dump(user_info, file)

def load_user_info():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            user_info = json.load(file)
            return user_info
    else:
        user_info = {}
        return user_info
    
def update_user_name(name):
    # global current_username
    user_data = load_user_info()

    if name not in user_data:
        user_data[name] = {"job": ''}
        # capture_user_image_and_train(name)
        save_user_info(user_data)
        # user_data["current_user"] = name
        # user_data["current_user_job"] = get_current_user_job(name)
    else:
        pass
        # If it's a new user, add them to the dictionary
        # user_data[name] = {"job": ''}
        # user_data["current_user"] = name
        # user_data["current_user_job"] = ''
        
        # capture_user_image_and_train(name)

    # save_user_info(user_data)

def update_user_job(job):
    user_data = load_user_info()

    user_data["current_user_job"] = job
    # user_data[get_current_user_name()] = {"job" : job}
    user_data[GLOBALS['current_face']] = {"job" : job}

    save_user_info(user_data)

def get_current_user_job(name):
    user_data = load_user_info()
    return user_data[name].get('job')