from modules.global_vars import GLOBALS
import random
from time import sleep
from hardware.eyelids_servo import blink_once
from hardware.head_servo import get_current_angles, smooth_head_servos_movement
from modules.global_vars import stop_random_movement
from hardware.servo_config import head_UD, right_TILT, left_TILT, head_LR

def random_movement():
    while True:
        if not GLOBALS['face_detected']:  
            stop_random_movement.clear()  # Allow random movement if no face is detected
            random_head_ud = random.randint(40, 100)
            random_head_lr = random.randint(70, 130)
            random_right_tilt = 90
            random_left_tilt = 180 - random_right_tilt

            current_angles = get_current_angles([head_UD, right_TILT, left_TILT, head_LR])
            target_angles = [random_head_ud, random_right_tilt, random_left_tilt, random_head_lr]

            smooth_head_servos_movement([head_UD, right_TILT, left_TILT, head_LR], current_angles, target_angles, steps=100)
            
            sleep(1)
        else:
            stop_random_movement.wait()  # Pause movement when face is detected


