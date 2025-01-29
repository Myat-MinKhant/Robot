from picamera2 import Picamera2
import cv2
import os
from modules.global_vars import GLOBALS
from modules.process_frame import process_frame
from modules.face_recognition import FaceRecognition

# Initialize Picamera2
camera = Picamera2()
camera.preview_configuration.main.size = (640, 480)
camera.start()  

def open_camera():
    global camera

    while GLOBALS['streaming']:
        frame = camera.capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame = cv2.flip(frame, 1)
        frame = process_frame(frame)
        
        cv2.imshow('Frame', frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    camera.stop()
    cv2.destroyAllWindows()


def capture_user_image_and_train(name):
    global streaming
    streaming = False
    picam2 = Picamera2()
    picam2.preview_configuration.main.size = (640, 480)
    picam2.preview_configuration.main.format = "RGB888"
    picam2.preview_configuration.align()
    picam2.configure("preview")
    picam2.start()
    frame = picam2.capture_array()
    
    image_filename = os.path.join('user_faces', f"{name}.jpg")
    cv2.imwrite(image_filename, frame)
    # cap.release()
    # picam2.stop()
    cv2.destroyAllWindows()

    # Reopen the camera with the updated known face encodings
    streaming = True
    fr = FaceRecognition()
    fr.encode_faces()
    fr.run_recognition()