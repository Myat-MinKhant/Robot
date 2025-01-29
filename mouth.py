import time
import nltk
import resources.phonemes as phonemes
# import subprocess
import threading
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)

upper_lip_channel = 0
jaw_channel = 1
left_cheek_channel = 2
right_cheek_channel = 3
DEFAULT_ANGLE = 90

# Defines
timePerPhoneme = 0.15
longPhonemeBonus = 0.05
smallPhonemeBonus = -0.05

# Load CMU Pronouncing Dictionary
entries = nltk.corpus.cmudict.entries()
print("Number of entries in CMU Dictionary:", len(entries))

# Function to move servos based on phoneme
def move_servos(angles):
    kit.servo[upper_lip_channel].angle = angles[0]
    kit.servo[jaw_channel].angle = angles[1]
    kit.servo[right_cheek_channel].angle = angles[2]
    kit.servo[left_cheek_channel].angle = angles[3]

    print(f"Servo positions set to: Upper Lip: {angles[0]}, Jaw: {angles[1]}, "
          f"Right Cheek: {angles[2]}, Left Cheek: {angles[3]}")

# Function to reset servos to default position
def reset_servos():
    kit.servo[upper_lip_channel].angle = DEFAULT_ANGLE
    kit.servo[jaw_channel].angle = 115
    kit.servo[left_cheek_channel].angle = 105
    kit.servo[right_cheek_channel].angle = DEFAULT_ANGLE

    print(f"Servos reset to default position: {DEFAULT_ANGLE}")

# # Function to speak text using espeak
# def speak_text(text):
#     subprocess.call(["espeak", "-s", "150", "-v", "en+f2", text])

# Function to process servos and phonemes
def process_servos(TextToSpeech):
    for word in TextToSpeech:
        timeForAWord = 0.0
        timeOfThisPhoneme = 0.0
        ServoMovements = []
        for ph in word[1]:
            if '1' in ph:
                timeForAWord += timePerPhoneme + longPhonemeBonus
                timeOfThisPhoneme = timePerPhoneme + longPhonemeBonus
            elif '0' in ph:
                timeForAWord += timePerPhoneme + smallPhonemeBonus
                timeOfThisPhoneme = timePerPhoneme + smallPhonemeBonus
            else:
                timeForAWord += timePerPhoneme
                timeOfThisPhoneme = timePerPhoneme

            if ph in phonemes.PhonemeToServo:
                ServoMovements.append((phonemes.PhonemeToServo[ph], timeOfThisPhoneme))

        # Move Servos
        for movement in ServoMovements:
            angles, duration = movement
            move_servos(angles)  # Pass the servo angles
            time.sleep(duration)

        # Reset servos to default position after each word
        reset_servos()

# Main loop to continuously get user input
while True:
    # Get user input
    user_input = input("Enter the text you want to process (or type 'exit' to quit): ")

    # Exit condition
    if user_input.lower() == 'exit':
        print("Exiting program.")
        break

    # Tokenize the user input
    tokens = nltk.word_tokenize(user_input)
    print("Tokens:", tokens)

    start_time = time.time()
    TextToSpeech = []
    for token in tokens:
        for entry in entries:
            if token.lower() == entry[0].lower():  # Case insensitive match
                TextToSpeech.append(entry)
                break
    end_time = time.time()

    # Debug!
    print("Pre-processing Done! Time: %s Seconds" % (end_time - start_time))

    # Start espeak and servo processing simultaneously
    # speech_thread = threading.Thread(target=speak_text, args=(user_input,))
    servo_thread = threading.Thread(target=process_servos, args=(TextToSpeech,))

    # Start threads
    # speech_thread.start()
    servo_thread.start()

    # Wait for both threads to finish
    # speech_thread.join()
    servo_thread.join()
