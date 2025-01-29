import cv2
from adafruit_servokit import ServoKit
from time import sleep

# Initialize ServoKit for 16 channels
kit = ServoKit(channels=16)
time = 0.015  # Time delay for smooth movement

# Define the servo channels
head_UD = 13      # Up/Down (vertical movement of head)
right_TILT = 5    # Right-side tilt
left_TILT = 12    # Left-side tilt
head_LR = 6       # Left/Right (horizontal movement of head)
eye_ud = 0        # Eye Up/Down
eye_lr = 1        # Eye Left/Right

# Helper function to get current servo angles
def get_current_angles(channels, defaults):
    return [kit.servo[channel].angle if kit.servo[channel].angle is not None else defaults[i] for i, channel in enumerate(channels)]

# Move servos simultaneously
def move_servos_simultaneously(channels, current_angles, target_angles):
    steps = 100  # Number of steps for smooth movement
    for step in range(steps):
        for i in range(len(channels)):
            delta = target_angles[i] - current_angles[i]
            new_angle = current_angles[i] + delta * step / steps
            kit.servo[channels[i]].angle = new_angle
        sleep(time)

# Reset servos to default angles
def reset_servos():
    current_angles = get_current_angles([head_UD, right_TILT, left_TILT, head_LR, eye_lr, eye_ud], [80, 90, 90, 90, 78, 78])
    move_servos_simultaneously([head_UD, right_TILT, left_TILT, head_LR, eye_lr, eye_ud], current_angles, [80, 90, 90, 90, 78, 78])

# OpenCV setup for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
esp32_url = 'http://192.168.1.7:81'
cap = cv2.VideoCapture(esp32_url)

frame_center_x = 320  # Assuming 640x480 camera resolution
frame_center_y = 240

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) > 0:
        # Get the largest detected face
        (x, y, w, h) = max(faces, key=lambda face: face[2] * face[3])

        # Calculate face center
        face_center_x = x + w // 2
        face_center_y = y + h // 2

        # Horizontal adjustment for head_LR and eye_lr
        horizontal_error = face_center_x - frame_center_x
        current_head_lr = get_current_angles([head_LR], [90])[0]
        current_eye_lr = get_current_angles([eye_lr], [78])[0]

        if abs(horizontal_error) > 20:  # Only move if error is significant
            if horizontal_error < 0:  # Face is to the left
                new_head_lr = max(20, current_head_lr - 1)  # Adjust within servo limits
                new_eye_lr = max(64, current_eye_lr - 1)
            else:  # Face is to the right
                new_head_lr = min(160, current_head_lr + 1)
                new_eye_lr = min(86, current_eye_lr + 1)
            move_servos_simultaneously([head_LR, eye_lr], [current_head_lr, current_eye_lr], [new_head_lr, new_eye_lr])

        # Vertical adjustment for head_UD and eye_ud
        vertical_error = face_center_y - frame_center_y
        current_head_ud = get_current_angles([head_UD], [80])[0]
        current_eye_ud = get_current_angles([eye_ud], [78])[0]

        if abs(vertical_error) > 20:  # Only move if error is significant
            if vertical_error < 0:  # Face is above center
                new_head_ud = max(30, current_head_ud - 1)
                new_eye_ud = max(64, current_eye_ud - 1)
            else:  # Face is below center
                new_head_ud = min(150, current_head_ud + 1)
                new_eye_ud = min(120, current_eye_ud + 1)
            move_servos_simultaneously([head_UD, eye_ud], [current_head_ud, current_eye_ud], [new_head_ud, new_eye_ud])

    # Display the frame for debugging
    cv2.imshow('Face Tracking', frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()
reset_servos()
