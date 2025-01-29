from adafruit_servokit import ServoKit
from time import sleep

kit = ServoKit(channels=16)  # Initialize ServoKit for 16 channels
time = 0.015  # Time delay for smooth movement

# Define the servo channels
head_UD = 13      # Up/Down (vertical movement of head)
right_TILT = 5   # Right-side tilt
left_TILT = 12    # Left-side tilt
head_LR = 6       # Left/Right (horizontal movement of head)
eye_ud = 0
eye_lr = 1

# Helper function to get current servo angles, with custom default values for each servo
def get_current_angles(channels, defaults):
    return [kit.servo[channel].angle if kit.servo[channel].angle is not None else defaults[i] for i, channel in enumerate(channels)]

# Move servos simultaneously
def move_servos_simultaneously(channels, current_angles, target_angles):
    steps = 100  # Number of steps for smooth movement
    max_delta = max([abs(target_angles[i] - current_angles[i]) for i in range(len(channels))])

    for step in range(steps):
        for i in range(len(channels)):
            delta = target_angles[i] - current_angles[i]
            new_angle = current_angles[i] + delta * step / steps
            kit.servo[channels[i]].angle = new_angle
        sleep(time)
    
    # Set servos to exact target angles at the end
    for i in range(len(channels)):
        kit.servo[channels[i]].angle = target_angles[i]

# Directional Movements
    
def look_left():
    current_angle = get_current_angles([eye_lr], [78])[0]
    move_servos_simultaneously([eye_lr], [current_angle], [64])
    
def look_right():
    current_angle = get_current_angles([eye_lr], [78])[0]
    move_servos_simultaneously([eye_lr], [current_angle], [86])
    
def look_up():
    current_angle = get_current_angles([eye_ud], [78])[0]
    move_servos_simultaneously([eye_ud], [current_angle], [64])
    
def look_down():
    current_angle = get_current_angles([eye_ud], [78])[0]
    move_servos_simultaneously([eye_ud], [current_angle], [120])
    
def down():
    current_angles = get_current_angles([head_UD, right_TILT, left_TILT], [80, 90, 90])
    move_servos_simultaneously([head_UD, right_TILT, left_TILT], current_angles, [150, 90, 90])

def up():
    current_angles = get_current_angles([head_UD, right_TILT, left_TILT], [80, 90, 90])
    move_servos_simultaneously([head_UD, right_TILT, left_TILT], current_angles, [30, 150, 90])

def left():
    current_angle = get_current_angles([head_LR], [90])[0]
    move_servos_simultaneously([head_LR], [current_angle], [20])

def right():
    current_angle = get_current_angles([head_LR], [90])[0]
    move_servos_simultaneously([head_LR], [current_angle], [160])

def front():
    current_angle = get_current_angles([head_LR], [90])[0]
    move_servos_simultaneously([head_LR], [current_angle], [90])

def tilt_left():
    current_angles = get_current_angles([right_TILT, left_TILT], [90, 90])
    move_servos_simultaneously([right_TILT, left_TILT], current_angles, [30, 150])

def tilt_right():
    current_angles = get_current_angles([right_TILT, left_TILT], [90, 90])
    move_servos_simultaneously([right_TILT, left_TILT], current_angles, [150, 30])

# Reset servos to default angles
def reset():
    current_angles = get_current_angles([head_UD, right_TILT, left_TILT, head_LR, eye_lr, eye_ud], [80, 90, 90, 90, 78, 78])
    move_servos_simultaneously([head_UD, right_TILT, left_TILT, head_LR, eye_lr, eye_ud], current_angles, [80, 90, 90, 90, 78, 78])

# Main loop to control the movement
while True:
    task = input('Enter direction (up, down, left, right, etc.): ')
    
    if task == 'down':
        down()
    elif task == 'up':
        up()
    elif task == 'left':
        left()
    elif task == 'right':
        right()
    elif task == 'front':
        front()
    elif task == 'tl':
        tilt_left()
    elif task == 'tr':
        tilt_right()
    elif task == 'lu':
        look_up()
    elif task == 'ld':
        look_down()
    elif task == 'll':
        look_left()
    elif task == 'lr':
        look_right()
    else: 
        reset()
