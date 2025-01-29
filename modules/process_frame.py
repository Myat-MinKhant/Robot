from modules.global_vars import GLOBALS
from modules.hand_tracking import HandTracking
from modules.face_recognition import FaceRecognition
from modules.object_detection import object_detection
from modules.talk import talk
import time

# Initialize face recognition
face_recog = FaceRecognition()
face_recog.encode_faces() 
timer = None

def process_frame(frame):
    if GLOBALS["task_changed"]:
        GLOBALS["task_changed"] = False
        GLOBALS["task_completed"] = False
        
    if GLOBALS["current_task"] == 'color_recognition':
        frame = object_detection(frame)
        
        if GLOBALS["current_object_detection"] is not None:
            GLOBALS["task_completed"] = True

            # Check if the user requested a specific object and it was detected
            if GLOBALS["user_requested_object"] and GLOBALS["current_object_detection"] == GLOBALS["user_requested_object"]:
                if GLOBALS["object_colors"]:
                    talk(f"The color of {GLOBALS['user_requested_object']} is {GLOBALS['object_colors']}.")
                    GLOBALS["user_requested_object"] = None
                    GLOBALS["object_colors"] = None
                else:
                    # If the requested object was not found in the color data
                    talk(f"I don't have color information for {GLOBALS['user_requested_object']}.")
                    GLOBALS["user_requested_object"] = None
            else:
                talk(f"I see {GLOBALS['object_colors']} {GLOBALS['current_object_detection']}.")
                GLOBALS["object_colors"] = None
                GLOBALS["current_object_detection"] = None
                
            GLOBALS["current_task"] = 'face_recognition'    # Change back to normal frame
        else:
            if timer is None:
                timer = time.time()
            elif time.time() - timer > 10:
                talk('I could not see the object clearly. Can you show a bit closer.')
                timer = time.time()
        
    elif GLOBALS["current_task"] == 'object_detection':
        frame = object_detection(frame)
        if GLOBALS["current_object_detection"] is not None:
            GLOBALS["task_completed"] = True

            if GLOBALS["user_requested_object"] and GLOBALS["user_requested_object"] == GLOBALS["current_object_detection"]:
                talk(f"Yes. I see {GLOBALS['user_requested_object']}.")
                GLOBALS["user_requested_object"] = None
            elif GLOBALS["user_requested_object"] and GLOBALS["user_requested_object"] != GLOBALS["current_object_detection"]:
                talk(f"I do not see {GLOBALS['user_requested_object']}. My camera detect {GLOBALS['current_object_detection']}.")
                GLOBALS["user_requested_object"] = None
            else:
                talk(f"I see {GLOBALS['current_object_detection']}")
                GLOBALS["current_object_detection"] = None
                GLOBALS["task_completed"] = False  # Reset task_completed after printing

            GLOBALS["current_task"] = 'face_recognition'      # Change back to normal frame
        else:
            if timer is None:
                timer = time.time()
            elif time.time() - timer > 10:
                talk('I could not see the object clearly. Can you show a bit closer.')
                timer = time.time()

    elif GLOBALS["current_task"] == 'face_recognition':
        frame = face_recog.run_recognition(frame)
        if not any([GLOBALS["current_face"], GLOBALS["task_completed"]]):
            GLOBALS["current_task"] = GLOBALS["previous_task"]
        else:
            GLOBALS["task_completed"] = True

    elif GLOBALS["current_task"] == 'hand_tracking':
        frame = HandTracking(frame)
        if GLOBALS["current_finger_count"] is not None:
            GLOBALS["task_completed"] = True 
            if GLOBALS["task_completed"]:
                talk(f"I see {GLOBALS['current_finger_count']} finger up.")
                GLOBALS["current_finger_count"] = None
                GLOBALS["task_completed"] = False
                GLOBALS["current_task"] = 'face_recognition'
        else:
            if timer is None:
                timer = time.time()
            elif time.time() - timer > 10:
                talk("I could not see your fingers clearly. Please show your hand closer to the camera.")
                timer = time.time()

    return frame