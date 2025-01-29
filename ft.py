from cvzone.FaceDetectionModule import FaceDetector
import cv2
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)

esp32_url = 'http://192.168.1.4:81'
cap = cv2.VideoCapture(esp32_url)
detector = FaceDetector()

x_position = 90
y_position = 90

kit.servo[6].angle = x_position
kit.servo[13].angle = y_position
while True:
    success, img = cap.read()
    
    if not success:
        break

    img = cv2.flip(img, 1)
    
    img, bboxs = detector.findFaces(img)

    if bboxs:
        # bboxInfo - "id","bbox","score","center"
        center1 = bboxs[0]["center"]
        x_medium = center1[0]
        y_medium = center1[1]
        a = x_medium // 62
        b = y_medium // 62
        
        print(b)
        
        # Swap the conditions to change left/right direction
        if 5 < a < 20:
            x_position -= 1.5  # Move left decreases angle
        elif 1 < a < 4:
            x_position += 1.5  # Move right increases angle
            
        if 5 < b < 20:
            y_position += 1.5
        elif 1 < b < 4:
            y_position -= 1.5
        
        # Set limits for position
        # position = max(30, min(y_position, 150))
        # kit.servo[6].angle = y_position
        
        position = max(30, min(y_position, 150))
        kit.servo[13].angle = y_position
    
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
