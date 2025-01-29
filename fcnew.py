import face_recognition
import cv2
import numpy as np
import math
import time
import os

# Function to calculate face confidence
def face_confidence(face_distance, face_match_threshold=0.6):
    range_val = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range_val * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value)) + '%'

class FaceRecognition_ObjectDetection:
    def __init__(self):
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.known_face_encodings = []
        self.known_face_names = []
        self.process_current_frame = True
        self.start_time = time.time()
        self.frame_count = 0
        self.net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
        self.classes = []
        with open("coco.names", "r") as f:
            self.classes = [line.strip() for line in f.readlines()]

    def encode_faces(self):
        for image in os.listdir('user_faces'):
            face_image = face_recognition.load_image_file(os.path.join('user_faces', image))
            face_encoding = face_recognition.face_encodings(face_image)[0]

            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(image.split('.')[0])

        print(self.known_face_names)

    def detect_objects(self, frame):
        height, width, _ = frame.shape
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)
        outs = self.net.forward(self.get_output_layers())
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5 and class_id in [ 65, 66, 76 ]:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = center_x - w / 2
                    y = center_y - h / 2
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])

        return boxes

    def get_output_layers(self):
        layer_names = self.net.getUnconnectedOutLayers()
        return [self.net.getLayerNames()[i[0] - 1 ] for i in layer_names]

    def run_camera(self):
        video_capture = cv2.VideoCapture(0)

        if not video_capture.isOpened():
            print('Video source not found.')
            return

        while True:
            ret, frame = video_capture.read()

            if self.process_current_frame:
                # YOLO object detection
                boxes = self.detect_objects(frame)

                # Face recognition
                # small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
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

                # Display annotation for YOLO object detection
                for box in boxes:
                    x, y, w, h = map(int, box)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Display annotation for face recognition
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

            # Display the frame
            cv2.imshow('Face and Object Recognition', frame)

            if cv2.waitKey(1) == ord('q'):
                break

        video_capture.release()
        cv2.destroyAllWindows()

fr = FaceRecognition_ObjectDetection()
fr.encode_faces()
fr.run_camera()
