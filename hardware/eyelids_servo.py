from adafruit_servokit import ServoKit
from time import sleep
import random
from modules.global_vars import GLOBALS
from hardware.servo_config import get_current_angles
from hardware.servo_config import *

kit = ServoKit(channels=16)

blink_duration =  random.uniform(0.1, 0.3)
blink_interval = random.uniform(3.5, 4.5)

def smooth_blink_servos_movement(channels, current_angles, target_angles, steps=10):
    step_delay = blink_duration / steps  # Adjust delay per step
    for step in range(steps + 1):
        for i, channel in enumerate(channels):
            delta = target_angles[i] - current_angles[i]
            new_angle = current_angles[i] + (delta * step / steps)
            kit.servo[channel].angle = round(new_angle)
        sleep(step_delay)

def blink_eyes():
    while True:
        if not GLOBALS['blink_natural']:
            sleep(0.1)
            continue
        else:
            current_angles = get_current_angles([r_upper_eyelids_servo_channel, r_lower_eyelids_servo_channel])

            smooth_blink_servos_movement([r_upper_eyelids_servo_channel, r_lower_eyelids_servo_channel], current_angles, [UPPER_EYE_LID_CLOSE, LOWER_EYE_LID_CLOSE])
            smooth_blink_servos_movement([r_upper_eyelids_servo_channel, r_lower_eyelids_servo_channel], [UPPER_EYE_LID_CLOSE, LOWER_EYE_LID_CLOSE], [UPPER_EYE_LID_OPEN, LOWER_EYE_LID_OPEN])

            sleep(blink_interval)

def blink_once():
    current_angles = get_current_angles([r_upper_eyelids_servo_channel, r_lower_eyelids_servo_channel])

    smooth_blink_servos_movement([r_upper_eyelids_servo_channel, r_lower_eyelids_servo_channel], current_angles, [UPPER_EYE_LID_CLOSE, LOWER_EYE_LID_CLOSE])
    smooth_blink_servos_movement([r_upper_eyelids_servo_channel, r_lower_eyelids_servo_channel], [UPPER_EYE_LID_CLOSE, LOWER_EYE_LID_CLOSE], [UPPER_EYE_LID_OPEN, LOWER_EYE_LID_OPEN])