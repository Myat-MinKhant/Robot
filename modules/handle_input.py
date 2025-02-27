from modules.global_vars import GLOBALS
from modules.empty_response import handle_empty_response
from modules.file_manager import save_conversation
from modules.talk import talk
from modules.preprocess import preprocess_response, get_openai_response


def handle_user_input(user_input, current_conversation, current_user_name):

    current_conversation.append(f"{current_user_name}: {user_input}")

    # Fetch response from OpenAI API
    response = get_openai_response("\n".join(current_conversation))

    # if response["choices"][0]["text"].strip() == "":
    if response == "":
        handle_empty_response()
    else:
        GLOBALS['empty_response_count'] = 0

    response_string = preprocess_response(response)
    # response_string = preprocess_response(response)

    current_conversation.append(f"{GLOBALS['bot_name']}: {response_string}")

    if current_user_name != "Guest":
        save_conversation(current_user_name, current_conversation)

    talk(response_string)