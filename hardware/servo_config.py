from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)

# Servo channels for head movement
r_eye_ud_servo_channel = 4
r_eye_lr_servo_channel = 5
r_upper_eyelids_servo_channel = 6
r_lower_eyelids_servo_channel = 7 

right_TILT = 11
left_TILT = 12
head_UD = 13
head_LR = 14 

# Servo angle limits
HEAD_LR_MIN, HEAD_LR_MAX = 20, 160
HEAD_UD_MIN, HEAD_UD_MAX = 20, 140
TILT_MIN, TILT_MAX = 90, 150
UPPER_EYE_LID_OPEN, UPPER_EYE_LID_CLOSE = 40, 105
LOWER_EYE_LID_OPEN, LOWER_EYE_LID_CLOSE = 80, 45
EYES_UD_MIN, EYES_UD_MAX = 64, 120
EYES_LR_MIN, EYES_LR_MAX = 70, 88 #63,88

DEFAULT_POSITIONS = {
    head_UD: 70,
    right_TILT: 90,
    left_TILT: 90,
    head_LR: 100,
    r_upper_eyelids_servo_channel: 40,  # Open
    r_lower_eyelids_servo_channel: 40,
    r_eye_ud_servo_channel: 78,
    r_eye_lr_servo_channel: 78,
}

def get_current_angles(channels):
    angles = [kit.servo[channel].angle if kit.servo[channel].angle is not None else DEFAULT_POSITIONS[channel] for channel in channels]
    return angles