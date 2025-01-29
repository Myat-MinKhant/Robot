from adafruit_servokit import ServoKit
import time
import nltk
import resources.phonemes as phonemes

# Initialize ServoKit
kit = ServoKit(channels=16)

# Servo channels
upper_lip_channel = 0
jaw_channel = 1
left_cheek_channel = 2
right_cheek_channel = 3
DEFAULT_ANGLE = 90

# Phoneme timing
timePerPhoneme = 0.15
longPhonemeBonus = 0.05
smallPhonemeBonus = -0.05

# Function to move servos
def move_servos(servo_movements):
    for angles, duration in servo_movements:
        kit.servo[upper_lip_channel].angle = angles[0]
        kit.servo[jaw_channel].angle = angles[1]
        kit.servo[right_cheek_channel].angle = angles[2]
        kit.servo[left_cheek_channel].angle = angles[3]
        time.sleep(duration)
    reset_servos()

# Reset servos to default position
def reset_servos():
    kit.servo[upper_lip_channel].angle = DEFAULT_ANGLE
    kit.servo[jaw_channel].angle = 115
    kit.servo[left_cheek_channel].angle = 105
    kit.servo[right_cheek_channel].angle = DEFAULT_ANGLE

def generate_servo_movements(response_string):
    print("Robot is thinking...")
    tokens = nltk.word_tokenize(response_string.lower())
    entries = nltk.corpus.cmudict.entries()

    servo_movements = []
    for token in tokens:
        for entry in entries:
            if token == entry[0].lower():
                for ph in entry[1]:
                    if '1' in ph:
                        duration = timePerPhoneme + longPhonemeBonus
                    elif '0' in ph:
                        duration = timePerPhoneme + smallPhonemeBonus
                    else:
                        duration = timePerPhoneme

                    if ph in phonemes.PhonemeToServo:
                        servo_movements.append((phonemes.PhonemeToServo[ph], duration))
                break
    return servo_movements