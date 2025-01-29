import cv2
import numpy as np
import tensorflow as tf
from picamera2 import Picamera2
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util
from cvzone.HandTrackingModule import HandDetector
import threading
import os
import face_recognition
import math

# Global variables for current states
current_face = None
current_object_detection = None
current_finger_count = None

# Global task and state management variables
current_task = None
task_changed = False
task_completed = False
stop_threads = False

def object_detection(frame):
    global current_object_detection, task_completed
    # Run object detection
    detections = run_inference_for_single_image(detect_fn, frame)

    # Filter out detections of people (class ID 1)
    person_class_id = 1
    indices = np.where(detections['detection_classes'] != person_class_id)[0]

    detections['detection_boxes'] = detections['detection_boxes'][indices]
    detections['detection_classes'] = detections['detection_classes'][indices]
    detections['detection_scores'] = detections['detection_scores'][indices]

    # Print detected object names
    if len(detections['detection_classes']) > 0:
        detected_object_names = [category_index[class_id]['name'] for class_id in detections['detection_classes']]
        current_object_detection = detected_object_names[0] if detected_object_names else None

    # Visualize the results of a detection
    vis_util.visualize_boxes_and_labels_on_image_array(
        frame,
        detections['detection_boxes'],
        detections['detection_classes'],
        detections['detection_scores'],
        category_index,
        use_normalized_coordinates=True,
        line_thickness=3)

    task_completed = True
    return frame

def hand_tracking(frame):
    global current_finger_count, task_completed
    hands, frame = detector.findHands(frame, draw=True)
    
    if hands:
        fingers_up = [detector.fingersUp(hand) for hand in hands]
        count_1 = sum([fingers.count(1) for fingers in fingers_up])
        current_finger_count = count_1
        
        cv2.putText(frame, f'Fingers Up: {count_1}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    
    task_completed = True
    return frame

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

    def encode_faces(self):
        for image in os.listdir('/home/pi/Desktop/Robot/user_faces'):
            face_image = face_recognition.load_image_file(os.path.join('/home/pi/Desktop/Robot/user_faces', image))
            face_encoding = face_recognition.face_encodings(face_image)[0]

            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(image.split('.')[0])

    def run_recognition(self, frame):
        global current_face, task_completed
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        self.face_locations = face_recognition.face_locations(rgb_small_frame, model='hog')
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

        self.process_current_frame = not self.process_current_frame

        for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 255, 0), 1)
        
        current_face = self.face_names[0] if self.face_names else None
        task_completed = True

        return frame

# Initialize Picamera2
camera = Picamera2()
camera.preview_configuration.main.size = (640, 480)
camera.start()

# Load the label map
PATH_TO_LABELS = '/home/pi/models/research/object_detection/data/mscoco_label_map.pbtxt'
category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)

# Load the model
PATH_TO_CKPT = '/home/pi/ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8/saved_model'
detect_fn = tf.saved_model.load(PATH_TO_CKPT)

# Initialize hand detector
detector = HandDetector(maxHands=2, detectionCon=0.5, minTrackCon=0.5)

# Initialize face recognition
face_recog = FaceRecognition()
face_recog.encode_faces()

def run_inference_for_single_image(model, image):
    # Convert the image to the expected format (uint8, 3 channels)
    image_np = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    input_tensor = tf.convert_to_tensor(image_np)
    input_tensor = input_tensor[tf.newaxis, ...]

    # Run inference
    detections = model(input_tensor)
    
    # Convert tensors to numpy arrays
    num_detections = int(detections.pop('num_detections'))
    detections = {key: value[0, :num_detections].numpy() for key, value in detections.items()}
    detections['num_detections'] = num_detections

    # Detection_classes should be ints
    detections['detection_classes'] = detections['detection_classes'].astype(np.int64)
    
    return detections

def process_frame(frame):
    global task_changed, task_completed
    if task_changed:
        print("Task changed, updating frame processing...")
        task_changed = False
        task_completed = False

    if current_task == 'object_detection':
        frame = object_detection(frame)
        if task_completed:
            print(f"Current object detection: {current_object_detection}")
    elif current_task == 'face_recognition':
        frame = face_recog.run_recognition(frame)
        if task_completed:
            print(f"Current face: {current_face}")
    elif current_task == 'hand_tracking':
        frame = hand_tracking(frame)
        if task_completed:
            print(f"Current finger count: {current_finger_count}")

    task_completed = False
    return frame

def listen_for_command():
    global current_task, task_changed

    while not stop_threads:
        command = input("Enter command: ").strip().lower()
        if 'what is this' in command:
            current_task = 'object_detection'
        elif 'who am i' in command:
            current_task = 'face_recognition'
        elif 'how many finger' in command:
            current_task = 'hand_tracking'
        else:
            current_task = None

        task_changed = True
        print(f"Current task: {current_task}")

# Start the command listener thread
command_thread = threading.Thread(target=listen_for_command)
command_thread.start()

# Main loop
try:
    while True:
        frame = camera.capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Process the frame based on the current task
        frame = process_frame(frame)

        # Display the frame
        cv2.imshow('Frame', frame)

        # Exit if 'esc' is pressed
        if cv2.waitKey(1) & 0xFF == 27:
            break
except KeyboardInterrupt:
    pass

# Stop the command listener thread
stop_threads = True
command_thread.join()

# Release resources
camera.stop()
cv2.destroyAllWindows()
