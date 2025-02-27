from modules.global_vars import GLOBALS
from cvzone.HandTrackingModule import HandDetector

detector = HandDetector(maxHands=2, detectionCon=0.5, minTrackCon=0.5)

def HandTracking(frame):
    # global current_finger_count, task_completed
    hands, frame = detector.findHands(frame, draw=True)
    if hands:
        fingers_up = [detector.fingersUp(hand) for hand in hands]
        count_1 = sum([fingers.count(1) for fingers in fingers_up])
        GLOBALS["current_finger_count"] = count_1
        # cv2.putText(frame, f'Fingers Up: {count_1}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    GLOBALS["task_completed"] = True
    return frame