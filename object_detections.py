import cv2
import numpy as np
import os

# Get the absolute path to the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load YOLO
cfg_path = os.path.join(script_dir, "yolov3.cfg")
weights_path = os.path.join(script_dir, "yolov3.weights")
names_path = os.path.join(script_dir, "coco.names")

net = cv2.dnn.readNet(weights_path, cfg_path)
classes = []
with open(names_path, "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getUnconnectedOutLayersNames()

# Video capture object
cap = cv2.VideoCapture(0)  # iPhone camera

while True:
    # Capture the frames
    ret, frame = cap.read()

    # Perform object detection
    height, width, _ = frame.shape
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (320, 320), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(layer_names)

    # Get bounding boxes and confidence for each detected object
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and class_id in [ 65, 66, 76]:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Non-maximum suppression to remove duplicate boxes
    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    # Draw bounding boxes and labels on the frame
    for i in range(len(boxes)):
        if i in indices:
            x, y, w, h = boxes[i]
            label = f"{classes[class_ids[i]]}: {confidences[i]:.2f}"
            color = (255, 0, 0)
            # if class_ids[i] == 0 else (255, 0, 0)  # Green for persons, blue for scissors, red for remotes
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Display the resulting frame
    cv2.imshow('Frame', frame)

    key = cv2.waitKey(1)
    if key == 27:  # Press 'esc' key to exit
        break

cap.release()
cv2.destroyAllWindows()
