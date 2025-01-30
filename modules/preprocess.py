import openai

def preprocess_response(response_string):
    response_string = response_string.replace("system: ", "").replace("Amora: ", "").replace("robot: ", "")
    index_of_john = response_string.find("john")
    response_string = response_string[:index_of_john]
    response_string = response_string.replace(" Is there anything else you would like to know", "")
    return response_string.strip()

def get_openai_response(prompt):
    return openai.Completion.create(
        engine='gpt-3.5-turbo-instruct',
        prompt=prompt,
        max_tokens=100,
        temperature=0.2,
    )