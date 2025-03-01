from time import sleep
from hardware.servo_config import *

time = 0.01  # Time delay for smooth movement

frame_center_x = 320
frame_center_y = 240

def smooth_head_servos_movement(channels, current_angles, target_angles, steps=10):
    for step in range(steps):
        for i in range(len(channels)):
            delta = target_angles[i] - current_angles[i]
            new_angle = current_angles[i] + (delta * step / steps)
            new_angle = round(new_angle)
            new_angle = max(min(new_angle, HEAD_LR_MAX if channels[i] == head_LR else HEAD_UD_MAX), HEAD_LR_MIN if channels[i] == head_LR else HEAD_UD_MIN)
            kit.servo[channels[i]].angle = new_angle
        sleep(time)

def generate_face_tracking(face_landmarks):
    x, y = int(face_landmarks.landmark[4].x * 640), int(face_landmarks.landmark[4].y * 480)

    # Horizontal
    horizontal_error = x - frame_center_x
    current_head_lr = get_current_angles([head_LR])[0]

    if abs(horizontal_error) > 20:
        Kp = 0.02
        new_head_lr = current_head_lr - (horizontal_error * Kp)
        new_head_lr = max(HEAD_LR_MIN, min(HEAD_LR_MAX, new_head_lr))
        new_head_lr = round(new_head_lr)

        if HEAD_LR_MIN <= new_head_lr <= HEAD_LR_MAX and abs(new_head_lr - current_head_lr) > 1:
            smooth_head_servos_movement([head_LR], [current_head_lr], [new_head_lr])

    # Vertical
    vertical_error = y - frame_center_y
    current_head_ud, current_right_tilt = get_current_angles([head_UD, right_TILT])

    if abs(vertical_error) > 20:
        new_head_ud = current_head_ud - 3 if vertical_error < 0 else current_head_ud + 3
        new_head_ud = round(new_head_ud)
        new_head_ud = max(HEAD_UD_MIN, min(HEAD_UD_MAX, new_head_ud))  # Keep within limits

        # Calculate right tilt proportionally
        tilt_ratio = (HEAD_UD_MAX - new_head_ud) / (HEAD_UD_MAX - HEAD_UD_MIN)
        new_right_tilt = round(TILT_MIN + (1 - tilt_ratio) * (TILT_MAX - TILT_MIN))
        smooth_head_servos_movement([head_UD, right_TILT], [current_head_ud, current_right_tilt], [new_head_ud, new_right_tilt])

# def generate_face_tracking(face_landmarks):
#     x, y = int(face_landmarks.landmark[4].x * 640), int(face_landmarks.landmark[4].y * 480)

#     # Horizontal
#     horizontal_error = x - frame_center_x
#     current_head_lr = get_current_angles([head_LR])[0]

#     if abs(horizontal_error) > 20:
#         Kp = 0.02
#         new_head_lr = current_head_lr - (horizontal_error * Kp)
#         new_head_lr = max(HEAD_LR_MIN, min(HEAD_LR_MAX, new_head_lr))
#         new_head_lr = round(new_head_lr)

#         if HEAD_LR_MIN <= new_head_lr <= HEAD_LR_MAX and abs(new_head_lr - current_head_lr) > 1:
#             smooth_head_servos_movement([head_LR], [current_head_lr], [new_head_lr])

#     # Vertical
#     vertical_error = y - frame_center_y
#     current_head_ud, current_right_tilt = get_current_angles([head_UD, right_TILT])

#     if abs(vertical_error) > 20:
#         new_head_ud = current_head_ud - 3 if vertical_error < 0 else current_head_ud + 3
#         new_head_ud = round(new_head_ud)
#         new_head_ud = max(HEAD_UD_MIN, min(HEAD_UD_MAX, new_head_ud))  # Keep within limits

#         # Calculate right tilt proportionally
#         tilt_ratio = (HEAD_UD_MAX - new_head_ud) / (HEAD_UD_MAX - HEAD_UD_MIN)
#         new_right_tilt = round(TILT_MIN + (1 - tilt_ratio) * (TILT_MAX - TILT_MIN))
#         smooth_head_servos_movement([head_UD, right_TILT], [current_head_ud, current_right_tilt], [new_head_ud, new_right_tilt])

# def generate_face_tracking(face_landmarks):
#     x, y = int(face_landmarks.landmark[4].x * 640), int(face_landmarks.landmark[4].y * 480)

#     # Get current servo positions
#     current_eye_lr, current_head_lr = get_current_angles([r_eye_lr_servo_channel, head_LR])
#     current_eye_ud, current_head_ud, current_right_tilt = get_current_angles([r_eye_ud_servo_channel, head_UD, right_TILT])

#     # Horizontal tracking
#     horizontal_error = x - frame_center_x

#     if abs(horizontal_error) > 3:  # Small error → move eyes first
#         Kp_eye = 0.03
#         new_eye_lr = current_eye_lr + (horizontal_error * Kp_eye)  # Eyes move opposite
#         new_eye_lr = max(EYES_LR_MIN, min(EYES_LR_MAX, new_eye_lr))
#         smooth_head_servos_movement([r_eye_lr_servo_channel], [current_eye_lr], [new_eye_lr])

#         # Move head if error is large
#         if abs(horizontal_error) > 100:
#             Kp_head = 0.02
#             new_head_lr = current_head_lr - (horizontal_error * Kp_head)  # Head moves normally
#             new_head_lr = max(HEAD_LR_MIN, min(HEAD_LR_MAX, new_head_lr))
#             smooth_head_servos_movement([head_LR], [current_head_lr], [new_head_lr])

#             # **Re-adjust eyes after head moves**
#             new_eye_lr = new_eye_lr + (horizontal_error * Kp_eye)  # Readjust slightly
#             new_eye_lr = max(EYES_LR_MIN, min(EYES_LR_MAX, new_eye_lr))
#             smooth_head_servos_movement([r_eye_lr_servo_channel], [new_eye_lr], [new_eye_lr])

#     # Vertical tracking
#     vertical_error = y - frame_center_y

#     if abs(vertical_error) > 3:  # Small error → move eyes first
#         Kp_eye = 0.03
#         new_eye_ud = current_eye_ud + (vertical_error * Kp_eye)  # Eyes move opposite
#         new_eye_ud = max(EYES_UD_MIN, min(EYES_UD_MAX, new_eye_ud))
#         smooth_head_servos_movement([r_eye_ud_servo_channel], [current_eye_ud], [new_eye_ud])

#         # Move head if error is large
#         if abs(vertical_error) > 100:
#             new_head_ud = current_head_ud - 3 if vertical_error < 0 else current_head_ud + 3
#             new_head_ud = max(HEAD_UD_MIN, min(HEAD_UD_MAX, new_head_ud))

#             # Adjust tilt proportionally
#             tilt_ratio = (HEAD_UD_MAX - new_head_ud) / (HEAD_UD_MAX - HEAD_UD_MIN)
#             new_right_tilt = round(TILT_MIN + (1 - tilt_ratio) * (TILT_MAX - TILT_MIN))

#             smooth_head_servos_movement([head_UD, right_TILT], [current_head_ud, current_right_tilt], [new_head_ud, new_right_tilt])

#             # **Re-adjust eyes after head moves**
#             new_eye_ud = new_eye_ud + (vertical_error * Kp_eye)  # Readjust slightly
#             new_eye_ud = max(EYES_UD_MIN, min(EYES_UD_MAX, new_eye_ud))
#             smooth_head_servos_movement([r_eye_ud_servo_channel], [new_eye_ud], [new_eye_ud])

# def generate_face_tracking(face_landmarks):
#     x, y = int(face_landmarks.landmark[4].x * 640), int(face_landmarks.landmark[4].y * 480)

#     # Get current positions
#     current_eye_lr, current_head_lr = get_current_angles([r_eye_lr_servo_channel, head_LR])
#     current_eye_ud, current_head_ud, current_right_tilt = get_current_angles([r_eye_ud_servo_channel, head_UD, right_TILT])

#     # Horizontal tracking
#     horizontal_error = x - frame_center_x

#     if abs(horizontal_error) > 3:  # Small error → move eyes first
#         Kp_eye = 0.03
#         new_eye_lr = current_eye_lr + (horizontal_error * Kp_eye)  # Eyes move opposite
#         new_eye_lr = max(EYES_LR_MIN, min(EYES_LR_MAX, new_eye_lr))
#         smooth_head_servos_movement([r_eye_lr_servo_channel], [current_eye_lr], [new_eye_lr])

#         # Move head if error is large
#         if abs(horizontal_error) > 100:
#             Kp_head = 0.02
#             new_head_lr = current_head_lr - (horizontal_error * Kp_head)  # Head moves normally
#             new_head_lr = max(HEAD_LR_MIN, min(HEAD_LR_MAX, new_head_lr))
#             smooth_head_servos_movement([head_LR], [current_head_lr], [new_head_lr])

#             # **Gradually move eyes back to center as head moves**
#             eye_return_speed = 0.02  # Slow return factor
#             new_eye_lr = (new_eye_lr * (1 - eye_return_speed)) + (DEFAULT_POSITIONS[r_eye_lr_servo_channel] * eye_return_speed)
#             smooth_head_servos_movement([r_eye_lr_servo_channel], [new_eye_lr], [new_eye_lr])

#     # Vertical tracking
#     vertical_error = y - frame_center_y

#     if abs(vertical_error) > 3:  # Small error → move eyes first
#         Kp_eye = 0.03
#         new_eye_ud = current_eye_ud + (vertical_error * Kp_eye)  # Eyes move opposite
#         new_eye_ud = max(EYES_UD_MIN, min(EYES_UD_MAX, new_eye_ud))
#         smooth_head_servos_movement([r_eye_ud_servo_channel], [current_eye_ud], [new_eye_ud])

#         # Move head if error is large
#         if abs(vertical_error) > 100:
#             new_head_ud = current_head_ud - 3 if vertical_error < 0 else current_head_ud + 3
#             new_head_ud = max(HEAD_UD_MIN, min(HEAD_UD_MAX, new_head_ud))

#             # Adjust tilt proportionally
#             tilt_ratio = (HEAD_UD_MAX - new_head_ud) / (HEAD_UD_MAX - HEAD_UD_MIN)
#             new_right_tilt = round(TILT_MIN + (1 - tilt_ratio) * (TILT_MAX - TILT_MIN))

#             smooth_head_servos_movement([head_UD, right_TILT], [current_head_ud, current_right_tilt], [new_head_ud, new_right_tilt])

#             # **Gradually move eyes back to center as head moves**
#             eye_return_speed = 0.02
#             new_eye_ud = (new_eye_ud * (1 - eye_return_speed)) + (DEFAULT_POSITIONS[r_eye_ud_servo_channel] * eye_return_speed)
#             smooth_head_servos_movement([r_eye_ud_servo_channel], [new_eye_ud], [new_eye_ud])
