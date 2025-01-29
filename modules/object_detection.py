import pandas as pd
import numpy as np
import cv2
import tensorflow as tf

from modules.global_vars import GLOBALS
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

# Load the label map and model
PATH_TO_LABELS = '/home/pi/Desktop/Robot/models/labels/research/object_detection/data/mscoco_label_map.pbtxt'
category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)
PATH_TO_CKPT = '/home/pi/Desktop/Robot/models/ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8/saved_model'
detect_fn = tf.saved_model.load(PATH_TO_CKPT)

index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
df = pd.read_csv('colors.csv', names=index, header=None)

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

# Function for object detection and color detection inside boxes
def object_detection(frame):
    # Run inference to detect objects
    detections = run_inference_for_single_image(detect_fn, frame)
    
    # Remove person class (optional, based on your needs)
    person_class_id = 1
    indices = np.where(detections['detection_classes'] != person_class_id)[0]
    detections['detection_boxes'] = detections['detection_boxes'][indices]
    detections['detection_classes'] = detections['detection_classes'][indices]
    detections['detection_scores'] = detections['detection_scores'][indices]
    
    # Get detected object names
    detected_object_names = [category_index[class_id]['name'] for class_id in detections['detection_classes']]
    GLOBALS["detected_objects"] = detected_object_names
    GLOBALS["current_object_detection"] = detected_object_names[0] if detected_object_names else None

    if GLOBALS["current_task"] == 'color_recognition' and detected_object_names:
        # Process only the top detected object (highest score)
        top_box = detections['detection_boxes'][0]
        ymin, xmin, ymax, xmax = top_box
        (im_height, im_width) = frame.shape[:2]
        (xmin, xmax, ymin, ymax) = (int(xmin * im_width), int(xmax * im_width), int(ymin * im_height), int(ymax * im_height))
        
        # Calculate the center point of the bounding box
        center_x = int((xmin + xmax) / 2)
        center_y = int((ymin + ymax) / 2)
        
        # Ensure the center point is within the bounding box
        if xmin <= center_x <= xmax and ymin <= center_y <= ymax:
            # Read the color from the center point of the bounding box
            b, g, r = frame[center_y, center_x]
            b, g, r = int(b), int(g), int(r)
            
            # Get the color name for the color at the center point
            color_name = getColorName(r, g, b)
            GLOBALS["object_colors"] = color_name  # Store the color

    # vis_util.visualize_boxes_and_labels_on_image_array(
    #     frame,
    #     detections['detection_boxes'],
    #     detections['detection_classes'],
    #     detections['detection_scores'],
    #     category_index,
    #     use_normalized_coordinates=True,
    #     line_thickness=3
    # )
    
    GLOBALS["task_completed"] = True
    return frame

# Function to get color name based on RGB values
def getColorName(R, G, B):
    minimum = 10000
    cname = "Unknown"
    for i in range(len(df)):
        d = abs(R - int(df.loc[i, "R"])) + abs(G - int(df.loc[i, "G"])) + abs(B - int(df.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = df.loc[i, 'color_name']
    return cname

# def get_color_name(r,g,b):
#     colors = {
#         'red': (255, 0, 0),
#         'green': (0, 255, 0),
#         'blue': (0, 0, 255),
#         'yellow': (255, 255, 0),
#         'cyan': (0, 255, 255),
#         'magenta': (255, 0, 255),
#         'white': (255, 255, 255),
#         'black': (0, 0, 0),
#         'gray': (128, 128, 128),
#         'orange': (255, 165, 0),
#         'pink': (255, 192, 203),
#         'purple': (128, 0, 128)
#     }
    
#     # Normalize the RGB values to avoid outliers from lighting conditions
#     rgb = np.array(rgb)
    
#     min_distance = float('inf')
#     closest_color = 'unknown'
    
#     for color_name, color_value in colors.items():
#         distance = np.sqrt(sum((rgb - np.array(color_value)) ** 2))
#         if distance < min_distance:
#             min_distance = distance
#             closest_color = color_name
    
#     return closest_color