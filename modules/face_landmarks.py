import cv2
import mediapipe as mp
from modules.global_vars import GLOBALS,  stop_random_movement
from hardware.head_servo import generate_face_tracking
from hardware.random_head_servo import random_movement
from hardware.eyelids_servo import blink_eyes

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

    def find_face_mesh_and_tracking(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(frame_rgb)

        if results.multi_face_landmarks:
            GLOBALS['face_detected'] = True
            GLOBALS['lost_face_counter'] = 0
            stop_random_movement.set()  # Stop random movement when face is detected

            for face_landmarks in results.multi_face_landmarks:
                # generate_face_tracking(face_landmarks)
                self.mp_drawing.draw_landmarks(
                    image=frame,
                    landmark_list=face_landmarks,
                    connections=self.connections,
                    landmark_drawing_spec=self.drawing_spec,
                    connection_drawing_spec=self.drawing_spec
                )
        else:
            GLOBALS['lost_face_counter'] += 1
            if GLOBALS['lost_face_counter'] > 10:
                GLOBALS['face_detected'] = False
                stop_random_movement.clear()  # Resume random movement if face is lost

        return frame
