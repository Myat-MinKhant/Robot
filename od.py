import cv2
import numpy as np
import os
import face_recognition
import math
import time
import cProfile

def face_confidence(face_distance, face_match_threshold=0.6):
    range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value)) + '%'

class FaceRecognition:
    def __init__(self):
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.known_face_encodings = []
        self.known_face_names = []
        self.process_current_frame = True
        self.start_time = time.time()
        self.frame_count = 0


    def encode_faces(self):
        for image in os.listdir('user_faces'):  # corrected path
            face_image = face_recognition.load_image_file(os.path.join('user_faces', image))  # corrected path
            face_encoding = face_recognition.face_encodings(face_image)[0]

            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(image.split('.')[0])  # remove file extension

        print(self.known_face_names) 

    def run_recognition_with_object_detection(self, yolo_net, yolo_classes, yolo_layer_names):
        video_capture = cv2.VideoCapture(0)

        if not video_capture.isOpened():
            print('Video source not found.')
            return

        while True:
            ret, frame = video_capture.read()

            if self.process_current_frame:
                # Resize the frame to a smaller resolution
                small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

                # small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

                # Perform object detection
                height, width, _ = frame.shape
                blob = cv2.dnn.blobFromImage(frame, 0.00392, (320, 320), (0, 0, 0), True, crop=False)
                yolo_net.setInput(blob)
                yolo_outs = yolo_net.forward(yolo_layer_names)

                # Get bounding boxes and confidence for each detected object
                yolo_class_ids = []
                yolo_confidences = []
                yolo_boxes = []
                for yolo_out in yolo_outs:
                    for detection in yolo_out:
                        scores = detection[5:]
                        yolo_class_id = np.argmax(scores)
                        confidence = scores[yolo_class_id]
                        if confidence > 0.5 and yolo_class_id in [65, 66, 76]:
                            center_x = int(detection[0] * width)
                            center_y = int(detection[1] * height)
                            w = int(detection[2] * width)
                            h = int(detection[3] * height)
                            x = int(center_x - w / 2)
                            y = int(center_y - h / 2)
                            yolo_boxes.append([x, y, w, h])
                            yolo_confidences.append(float(confidence))
                            yolo_class_ids.append(yolo_class_id)

                # Non-maximum suppression to remove duplicate boxes
                yolo_indices = cv2.dnn.NMSBoxes(yolo_boxes, yolo_confidences, 0.5, 0.4)

                # Draw bounding boxes and labels on the frame for YOLO
                for i in range(len(yolo_boxes)):
                    if i in yolo_indices:
                        x, y, w, h = yolo_boxes[i]
                        label = f"{yolo_classes[yolo_class_ids[i]]}: {yolo_confidences[i]:.2f}"
                        color = (255, 0, 0)  # Change color based on your preference
                        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                        cv2.putText(frame, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                # Face recognition (unchanged)
                self.face_locations = face_recognition.face_locations(rgb_small_frame)
                self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

                self.face_names = []
                for encoding in self.face_encodings:
                    matches = face_recognition.compare_faces(self.known_face_encodings, encoding)
                    name = 'Unknown'
                    confidence = 'Unknown'

                    face_distances = face_recognition.face_distance(self.known_face_encodings, encoding)
                    best_match_index = np.argmin(face_distances)

                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]
                        confidence = face_confidence(face_distances[best_match_index])

                    self.face_names.append(f'{name}, {confidence}')

                # Draw bounding boxes and labels on the frame for face recognition
                for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4

                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

                    # Display the name at the top-right corner
                    text_size, _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_DUPLEX, 0.8, 1)
                    cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 255, 0), 1)

            self.frame_count += 1
            elapsed_time = time.time() - self.start_time

            # Calculate and display fps every 5 seconds
            if elapsed_time > 5:
                fps = self.frame_count / elapsed_time
                print(f"Current frame fps: {fps:.2f}")
                self.start_time = time.time()
                self.frame_count = 0

            self.process_current_frame = not self.process_current_frame

            # Display the resulting frame
            cv2.imshow('Face Recognition with Object Detection', frame)

            key = cv2.waitKey(1)
            if key == 27:  # Press 'esc' key to exit
                break

        video_capture.release()
        cv2.destroyAllWindows()


# Set backend to use CUDA if available
# net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
# net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

# Initialize FaceRecognition instance
fr = FaceRecognition()
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load YOLO
yolo_cfg_path = os.path.join(script_dir, "yolov3.cfg")
yolo_weights_path = os.path.join(script_dir, "yolov3.weights")
yolo_names_path = os.path.join(script_dir, "coco.names")

yolo_net = cv2.dnn.readNet(yolo_weights_path, yolo_cfg_path)
yolo_classes = []
with open(yolo_names_path, "r") as f:
    yolo_classes = [line.strip() for line in f.readlines()]
yolo_layer_names = yolo_net.getUnconnectedOutLayersNames()

# Run face recognition with object detection
# cProfile.run('fr.encode_faces()')
fr.encode_faces()
cProfile.run('fr.run_recognition_with_object_detection(yolo_net, yolo_classes, yolo_layer_names)')
# fr.run_recognition_with_object_detection(yolo_net, yolo_classes, yolo_layer_names)
