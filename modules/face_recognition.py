import os
import cv2
import numpy as np
import face_recognition
from modules.global_vars import GLOBALS
from models.face_encoding import face_confidence

class FaceRecognition:
    def __init__(self):
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.known_face_encodings = []
        self.known_face_names = []
        self.process_current_frame = True

    def encode_faces(self):
        for image in os.listdir('resources/user_faces'):
            face_image = face_recognition.load_image_file(os.path.join('resources/user_faces', image))
            face_encoding = face_recognition.face_encodings(face_image)[0]
            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(image.split('.')[0])

    def run_recognition(self, frame):
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
                GLOBALS["current_face"] = name
                recognized = True

            self.face_names.append(f'{name}, {confidence}')

        if not recognized:
            GLOBALS["current_face"] = None

        for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            # cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 255, 0), 1)

        GLOBALS["task_completed"] = True
        return frame