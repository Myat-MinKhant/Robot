import cv2
import numpy as np

def count_fingers(frame, hand_contour):
    # Get bounding box of the hand
    x, y, w, h = cv2.boundingRect(hand_contour)

    # Extract the region of interest (ROI) containing the hand
    hand_roi = frame[y:y+h, x:x+w]

    # Convert the ROI to grayscale
    hand_gray = cv2.cvtColor(hand_roi, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur
    hand_blur = cv2.GaussianBlur(hand_gray, (5, 5), 0)

    # Thresholding
    _, hand_thresh = cv2.threshold(hand_blur, 100, 255, cv2.THRESH_BINARY_INV)

    # Find contours in the thresholded image
    contours, _ = cv2.findContours(hand_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Count fingers based on the number of fingers touching the bounding box
    finger_count = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 10000000000000:  # Adjust this threshold based on your scenario
            finger_count += 1

    return finger_count

# Open the webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Flip the frame horizontally for a later selfie-view display
    frame = cv2.flip(frame, 1)

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Thresholding
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Find the contour with the largest area
        max_contour = max(contours, key=cv2.contourArea)

        # Draw the hand contour on the frame
        cv2.drawContours(frame, [max_contour], 0, (0, 255, 0), 2)

        # Count fingers
        finger_count = count_fingers(frame, max_contour)

        # Display the finger count
        cv2.putText(frame, f"Fingers: {finger_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the result
    cv2.imshow("Hand Tracking and Finger Counting", frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
