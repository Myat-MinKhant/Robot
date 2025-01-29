from picamera2 import Picamera2
import time

picam2 = Picamera2()
picam2.start_preview()

# Give time for camera to initialize
time.sleep(2)

# Capture an image
picam2.capture_file("/home/pi/test_image.jpg")

picam2.stop_preview()
