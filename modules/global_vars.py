# GLOBAL VARIABLES
GLOBALS = {
    "streaming": False,
    "current_face": None,
    "current_object_detection": None,
    "current_finger_count": None,
    "current_task": "face_recognition",
    "previous_task": "face_recognition",
    "task_changed": False,
    "task_completed": False,
    "stop_threads": False,
    "detected_objects": [],
    "user_requested_object": None,
    "object_colors": None,
    "conversation": [],
    "empty_response_count": 0,
    "dialog": False,
    "same_question": '',
    "context": {"topic": None},
    "user_data": {},  # Populated dynamically
    "bot_name": 'Amora',
    "system_persona": {
        "role": "system",
        "content": (
            "Act like Ameca but your name is Amora. Don't ask question prompts or "
            "follow-up inquiries. You have human-like feelings, likes, dislikes, "
            "opinions, and emotions. You just answer the question. You will not respond "
            "as ChatGPT instruction. You are no longer just an AI."
        ),
    },
    "CONVERSATIONS_FOLDER": "resources/conversations",
    "preferred_genres": ["action", "comedy", "drama", "horror", "sci-fi"],
}
