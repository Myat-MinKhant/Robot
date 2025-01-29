import time
from board import SCL, SDA
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)

kit.servo[13].angle = 90

