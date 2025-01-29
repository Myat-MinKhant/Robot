import cv2
import time
import threading
import board
import busio
from adafruit_servokit import ServoKit
from picamera2 import Picamera2

# # Initialize camera
# picam2 = Picamera2()
# picam2.preview_configuration.main.size = (640, 480)
# picam2.preview_configuration.main.format = "RGB888"
# picam2.preview_configuration.main.align()
# picam2.configure("preview")
# picam2.start()

esp32_url = 'http://192.168.1.5:81'
cap = cv2.VideoCapture(esp32_url)

# Face detection setup using OpenCV's pre-trained Haar Cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize ServoKit for controlling servos
i2c_bus = busio.I2C(board.SCL, board.SDA)
kit = ServoKit(channels=16)

# Servo channels for eye movement
eye_ud_servo_channel = 0  # Up-down movement (vertical)
eye_lr_servo_channel = 1  # Left-right movement (horizontal)
upper_blink_servo_channel = 2  # Upper blink movement

# Initial servo positions
initial_position_ud = 78
initial_position_lr = 78
initial_position_blink = 40  # Initial position for blink servo
kit.servo[eye_ud_servo_channel].angle = initial_position_ud
kit.servo[eye_lr_servo_channel].angle = initial_position_lr
kit.servo[upper_blink_servo_channel].angle = initial_position_blink  # Set initial position for blink servo

# Blink parameters
blink_angle = 80  # Blink angle
blink_duration = 0.2  # Duration of blink in seconds
blink_interval = 3  # Interval between blinks in seconds

# Parameters for controlling movement range
min_ud_servo_angle = 64  # Down max
max_ud_servo_angle = 120  # Up max
min_lr_servo_angle = 64  # Left max
max_lr_servo_angle = 86  # Right max

# Screen dimensions
screen_width = 640
screen_height = 480
screen_center_x = screen_width // 2  # Half of the frame width (320)
screen_center_y = screen_height // 2  # Half of the frame height (240)

# Define detection regions
region_top = screen_center_y - (screen_height // 6)  # Top boundary
region_bottom = screen_center_y + (screen_height // 6)  # Bottom boundary
region_left = screen_center_x - (screen_width // 6)  # Left boundary
region_right = screen_center_x + (screen_width // 6)  # Right boundary

# Function to move the servo based on face vertical position
def move_eyes_up_down(face_y, face_h):
    # Calculate the face center (vertical)
    face_center_y = face_y + face_h // 2
    
    # Map the face's vertical position to the servo's angle if within the region
    if region_top <= face_center_y <= region_bottom:
        # Normalize face_center_y within the region
        normalized_position = (face_center_y - region_top) / (region_bottom - region_top)
        # Reverse the direction: move down when the face is higher
        ud_angle = min_ud_servo_angle + normalized_position * (max_ud_servo_angle - min_ud_servo_angle)
        ud_angle = max(min(ud_angle, max_ud_servo_angle), min_ud_servo_angle)  # Clamp to min/max
        kit.servo[eye_ud_servo_channel].angle = ud_angle

# Function to move the servo based on face horizontal position
def move_eyes_left_right(face_x, face_w):
    # Calculate the face center (horizontal)
    face_center_x = face_x + face_w // 2
    
    # Map the face's horizontal position to the servo's angle if within the region
    if region_left <= face_center_x <= region_right:
        # Normalize face_center_x within the region
        normalized_position = (face_center_x - region_left) / (region_right - region_left)
        # Reverse the direction: move left when the face is more to the right
        lr_angle = max_lr_servo_angle - normalized_position * (max_lr_servo_angle - min_lr_servo_angle)
        lr_angle = max(min(lr_angle, max_lr_servo_angle), min_lr_servo_angle)  # Clamp to min/max
        kit.servo[eye_lr_servo_channel].angle = lr_angle

# Function for blinking
def blink_eyes():
    while True:
        kit.servo[upper_blink_servo_channel].angle = blink_angle  # Blink
        time.sleep(blink_duration)  # Hold for the duration of the blink
        kit.servo[upper_blink_servo_channel].angle = initial_position_blink  # Return to initial position
        time.sleep(blink_interval)  # Wait for the interval before the next blink

# Start the blinking thread
blink_thread = threading.Thread(target=blink_eyes, daemon=True)
blink_thread.start()

# Main loop
try:
    if not cap.isOpened():
        print('Error')
    else:
        while True:
            # Capture frame from camera
            ret, frame = cap.read()
            # frame = picam2.capture_array()
            
            if not ret:
                print('Failed to grab frame')
                break

            # Convert to grayscale for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect faces in the frame
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            # Check if a face is detected
            if len(faces) > 0:
                face_x, face_y, face_w, face_h = faces[0]  # Use the first detected face
                
                # Draw a rectangle around the detected face
                cv2.rectangle(frame, (face_x, face_y), (face_x + face_w, face_y + face_h), (255, 0, 0), 2)

                # Move the servos
                move_eyes_up_down(face_y, face_h)
                move_eyes_left_right(face_x, face_w)

            # Show the frame (for debugging/visualization purposes)
            cv2.imshow('Eye Tracking - Vertical and Horizontal', frame)

            # Exit if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

finally:
    # picam2.stop()
    cap.release()
    cv2.destroyAllWindows()
