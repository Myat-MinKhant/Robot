import cv2
import mediapipe as mp
from picamera2 import Picamera2
import time
import os
import face_recognition
import numpy as np
import math

# Define global variables for face recognition
current_face = None
task_completed = False

def face_confidence(face_distance, face_match_threshold=0.6):
    range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value)) + '%'

class Picamera2Stream:
    def __init__(self, resolution=(640, 480)):
        self.camera = Picamera2()
        self.camera.preview_configuration.main.size = resolution
        self.camera.start()

    def get_frame(self):
        frame = self.camera.capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        return frame

    def __del__(self):
        self.camera.stop()

class FaceMeshDetector:
    def __init__(self, max_faces=1, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=max_faces,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence)

        self.drawing_spec = self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1)
        
        # Manually define specific face parts
        self.connections = self.get_connections()

    def get_connections(self):
        FACEMESH_FACE_OVAL = frozenset([
            (10, 338), (338, 297), (297, 332), (332, 284), (284, 251), (251, 389),
            (389, 356), (356, 454), (454, 323), (323, 361), (361, 288), (288, 397),
            (397, 365), (365, 379), (379, 378), (378, 400), (400, 377), (377, 152),
            (152, 148), (148, 176), (176, 149), (149, 150), (150, 136), (136, 172),
            (172, 58), (58, 132), (132, 93), (93, 234), (234, 127), (127, 162),
            (162, 21), (21, 54), (54, 103), (103, 67), (67, 109), (109, 10)
        ])

        FACEMESH_LEFT_EYE = frozenset([
            (33, 7), (7, 163), (163, 144), (144, 145), (145, 153), (153, 154),
            (154, 155), (155, 133), (33, 246), (246, 161), (161, 160), (160, 159),
            (159, 158), (158, 157), (157, 173), (173, 33)
        ])

        FACEMESH_LEFT_EYEBROW = frozenset([
            (70, 63), (63, 105), (105, 66), (66, 107), (107, 55), (70, 46), (46, 53),
            (53, 52), (52, 65), (65, 55)
        ])

        FACEMESH_RIGHT_EYE = frozenset([
            (263, 249), (249, 390), (390, 373), (373, 374), (374, 380), (380, 381),
            (381, 382), (382, 362), (263, 466), (466, 388), (388, 387), (387, 386),
            (386, 385), (385, 384), (384, 398), (398, 263)
        ])

        FACEMESH_RIGHT_EYEBROW = frozenset([
            (336, 296), (296, 334), (334, 293), (293, 300), (300, 276), (336, 285),
            (285, 295), (295, 282), (282, 283), (283, 276)
        ])

        FACEMESH_UPPER_LIP = frozenset([
            (61, 146), (146, 91), (91, 181), (181, 84), (84, 17), (17, 314),
            (314, 405), (405, 321), (321, 375), (375, 291), (61, 185), (185, 40),
            (40, 39), (39, 37), (37, 0), (0, 267), (267, 269), (269, 270),
            (270, 409), (409, 291)
        ])

        FACEMESH_LOWER_LIP = frozenset([
            (78, 95), (95, 88), (88, 178), (178, 87), (87, 14), (14, 317),
            (317, 402), (402, 318), (318, 324), (324, 308), (78, 191), (191, 80),
            (80, 81), (81, 82), (82, 13), (13, 312), (312, 311), (311, 310),
            (310, 415), (415, 308)
        ])

        FACEMESH_NOSE = frozenset([
            (1, 2), (2, 98), (98, 327), (327, 326), (326, 2)
        ])

        connections = FACEMESH_FACE_OVAL | FACEMESH_LEFT_EYE | FACEMESH_LEFT_EYEBROW | \
                      FACEMESH_RIGHT_EYE | FACEMESH_RIGHT_EYEBROW | FACEMESH_UPPER_LIP | \
                      FACEMESH_LOWER_LIP | FACEMESH_NOSE

        return connections

    def find_face_mesh(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(frame_rgb)
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                self.mp_drawing.draw_landmarks(
                    image=frame,
                    landmark_list=face_landmarks,
                    connections=self.connections,
                    landmark_drawing_spec=self.drawing_spec,
                    connection_drawing_spec=self.drawing_spec)
        return frame

class FaceRecognition:
    def __init__(self):
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.known_face_encodings = []
        self.known_face_names = []
        self.process_current_frame = True

    def encode_faces(self):
        for image in os.listdir('user_faces'):
            face_image = face_recognition.load_image_file(os.path.join('user_faces', image))
            face_encoding = face_recognition.face_encodings(face_image)[0]
            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(image.split('.')[0])

    def run_recognition(self, frame):
        global current_face, task_completed
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        self.face_locations = face_recognition.face_locations(rgb_small_frame, model='hog')
        self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

        recognized = False
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
                current_face = name
                recognized = True

            self.face_names.append(f'{name}, {confidence}')

        if not recognized:
            current_face = None

        for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            # cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 255, 0), 1)

        task_completed = True
        return frame

def main():
    camera = Picamera2Stream()
    detector = FaceMeshDetector()
    recognition = FaceRecognition()
    recognition.encode_faces()

    pTime = 0
    while True:
        frame = camera.get_frame()

        # Run face recognition
        frame = recognition.run_recognition(frame)

        # Run face mesh detection
        frame = detector.find_face_mesh(frame)
        
        # Calculate and display FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(frame, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

        # Display the frame
        cv2.imshow('Face Mesh Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.__del__()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
