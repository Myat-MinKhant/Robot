import cv2
import tensorflow as tf
import numpy as np
from picamera2 import Picamera2
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util
import pandas as pd
import imutils

# Initialize Picamera2
camera = Picamera2()
camera.preview_configuration.main.size = (640, 480)
camera.start()

streaming = False
current_face = None
current_object_detection = None
current_finger_count = None
current_task = 'face_recognition'
previous_task = 'face_recognition'
task_changed = False
task_completed = False
stop_threads = False
timer = False
detected_objects = []
user_requested_object = None 
object_colors = []

# Load the label map and model
PATH_TO_LABELS = '/home/pi/Desktop/Robot/models/research/object_detection/data/mscoco_label_map.pbtxt'
category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)
PATH_TO_CKPT = '/home/pi/Desktop/Robot/ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8/saved_model'
detect_fn = tf.saved_model.load(PATH_TO_CKPT)

# Load color names data
index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
df = pd.read_csv('colors.csv', names=index, header=None)

def getColorName(R, G, B):
    """Return the color name closest to the detected RGB value."""
    minimum = 10000
    cname = "Unknown"
    for i in range(len(df)):
        d = abs(R - int(df.loc[i, "R"])) + abs(G - int(df.loc[i, "G"])) + abs(B - int(df.loc[i, "B"]))
        if d < minimum:
            minimum = d
            cname = df.loc[i, 'color_name'] + '   Hex=' + df.loc[i, 'hex']
    return cname

def run_inference_for_single_image(model, image):
    image_np = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    input_tensor = tf.convert_to_tensor(image_np)
    input_tensor = input_tensor[tf.newaxis, ...]
    detections = model(input_tensor)
    num_detections = int(detections.pop('num_detections'))
    detections = {key: value[0, :num_detections].numpy() for key, value in detections.items()}
    detections['num_detections'] = num_detections
    detections['detection_classes'] = detections['detection_classes'].astype(np.int64)
    return detections


def object_detection(frame):
    global current_object_detection, task_completed, detected_objects, object_colors
    detections = run_inference_for_single_image(detect_fn, frame)
    
    # Detect non-person objects
    person_class_id = 1
    indices = np.where(detections['detection_classes'] != person_class_id)[0]
    detections['detection_boxes'] = detections['detection_boxes'][indices]
    detections['detection_classes'] = detections['detection_classes'][indices]
    detections['detection_scores'] = detections['detection_scores'][indices]
    
    detected_object_names = [category_index[class_id]['name'] for class_id in detections['detection_classes']]
    detected_objects = detected_object_names  # Store detected objects
    current_object_detection = detected_object_names[0] if detected_object_names else None
    
    object_colors = []  # List to store colors of detected objects
    display_strs = []  # List to store label strings with color
    
    for i, box in enumerate(detections['detection_boxes']):
        y_min, x_min, y_max, x_max = box  # Extract the bounding box coordinates
        y_min = int(y_min * frame.shape[0])
        x_min = int(x_min * frame.shape[1])
        y_max = int(y_max * frame.shape[0])
        x_max = int(x_max * frame.shape[1])
        
        roi = frame[y_min:y_max, x_min:x_max]  # Region of interest (ROI) within the bounding box

        # Calculate the mean of RGB values inside the ROI
        avg_color_per_row = np.average(roi, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0)

        # Get the R, G, B values
        b, g, r = avg_color
        b = int(b)
        g = int(g)
        r = int(r)
        
        # Get color name
        color_name = getColorName(r, g, b)

        # Store object color and name
        object_colors.append((detected_object_names[i], color_name))
        display_str = f'{detected_object_names[i]}: {color_name}'
        display_strs.append(display_str)

        # Update label map
        category_index[detections['detection_classes'][i]]['name'] = display_str
    
    vis_util.visualize_boxes_and_labels_on_image_array(
        frame,
        detections['detection_boxes'],
        detections['detection_classes'],
        detections['detection_scores'],
        category_index,
        use_normalized_coordinates=True,
        line_thickness=3
    )
    
    task_completed = True
    return frame

def open_camera():
    global streaming, camera

    while True:
        frame = camera.capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        kernal = np.ones((5, 5), "uint8")
        frame = object_detection(frame)
        
        cv2.imshow('Frame', frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    camera.stop()
    cv2.destroyAllWindows()

while True:
    open_camera()