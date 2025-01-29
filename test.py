import numpy as np
import pandas as pd
import cv2
from picamera2 import Picamera2
import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

camera = Picamera2()
camera.preview_configuration.main.size = (1280, 720)
camera.start()

detected_objects = []
user_requested_object = None 
object_colors = []

# Load the label map and model
PATH_TO_LABELS = '/home/pi/Desktop/Robot/models/research/object_detection/data/mscoco_label_map.pbtxt'
category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)
PATH_TO_CKPT = '/home/pi/Desktop/Robot/ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8/saved_model'
detect_fn = tf.saved_model.load(PATH_TO_CKPT)

index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
df = pd.read_csv('colors.csv', names=index, header=None)

# Function to get color name based on RGB values
def getColorName(R, G, B):
    minimum = 10000
    cname = "Unknown"
    for i in range(len(df)):
        d = abs(R - int(df.loc[i, "R"])) + abs(G - int(df.loc[i, "G"])) + abs(B - int(df.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = df.loc[i, 'color_name'] + '   Hex=' + df.loc[i, 'hex']
    return cname

# Function to run inference on the image
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
    global current_object_detection, task_completed, detected_objects, object_colors
    
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
    detected_objects = detected_object_names
    current_object_detection = detected_object_names[0] if detected_object_names else None
    
    if detected_object_names:
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
            object_colors = [(detected_object_names[0], color_name)]  # Store the top object name and its color
            
            # Annotate the color name on the frame
            # Optionally, mark the center of the bounding box
            cv2.circle(frame, (center_x, center_y), 5, (255, 255, 255), -1)
            
            # Create a rectangle at the top of the frame with the detected color
            cv2.rectangle(frame, (20, 20), (800, 60), (b, g, r), -1)
            text = f"{color_name}   R={r} G={g} B={b}"
            
            # Adjust text color based on brightness
            if r + g + b >= 600:
                cv2.putText(frame, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
            else:
                cv2.putText(frame, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

    # Visualize bounding boxes and labels on the frame
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

# def getColorName(R, G, B):
#     minimum = 10000
#     cname = "Unknown"
#     for i in range(len(df)):
#         d = abs(R - int(df.loc[i, "R"])) + abs(G - int(df.loc[i, "G"])) + abs(B - int(df.loc[i, "B"]))
#         if d <= minimum:
#             minimum = d
#             cname = df.loc[i, 'color_name'] + '   Hex=' + df.loc[i, 'hex']
#     return cname

# def identify_color(event, x, y, flags, param):
#     global b, g, r, xpos, ypos, clicked
#     if event == cv2.EVENT_LBUTTONDBLCLK:  # If double-click, capture the color
#         xpos = x
#         ypos = y
#         b, g, r = frame[y, x]
#         b = int(b)
#         g = int(g)
#         r = int(r)
#         clicked = True

# cv2.namedWindow('image')
# cv2.setMouseCallback('image', identify_color)

while True:
    frame = camera.capture_array()
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    
    kernal = np.ones((5, 5), "uint8")
    
    frame = object_detection(frame)
    
    cv2.imshow('image', frame)
    
    # Break the loop on pressing 'Esc'
    if cv2.waitKey(20) & 0xFF == 27:
        break

camera.stop()  # Properly stop the camera
cv2.destroyAllWindows()
