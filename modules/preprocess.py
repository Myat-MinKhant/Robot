import openai
import requests
import json

API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

def preprocess_response(response_string):
    response_string = response_string.replace("system: ", "").replace("Amora: ", "").replace("robot: ", "").replace("role: ", "").replace("content: ", "")
    index_of_john = response_string.find("john")
    response_string = response_string[:index_of_john]
    response_string = response_string.replace(" Is there anything else you would like to know", "")
    return response_string.strip()

def get_openai_response(prompt):
    # return openai.Completion.create(
    #     engine='gpt-3.5-turbo-instruct',
    #     prompt=prompt,
    #     max_tokens=100,
    #     temperature=0.2,
    # )
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
        },
        data=json.dumps({
            "model": "openai/gpt-3.5-turbo",  # Use chat model
            "messages": [
                {
                "role": "user",
                "content": prompt,
                "max_tokens": 100,
                "temperature": 0.2
                },
    ]
        })
        )

    response_data = response.json()

    if "choices" in response_data and response_data["choices"]:
        return response_data["choices"][0]["message"]["content"]
    else:
        return "api diff"
    
pdf_conversation_history = []

def get_pdf_response(query, context):

    pdf_conversation_history.append({"role": "user", "content": query})

    prompt = (
        "You are an assistant that can only answer questions using the provided document. "
        "If the answer cannot be found in the document, please respond with the exact text: NO_INFO. \n\n"
        "Document:\n"
        f"{context}\n\n"
        "Previous conversation:\n"
    )

    # Add the conversation history to the prompt (up to a limit, to avoid too long a prompt)
    for message in pdf_conversation_history[-10:]: 
        prompt += f"{message['role']}: {message['content']}\n"

    prompt += "Question:\n" + query + "\nAnswer:"

    try:
        response = requests.post(
            url=API_URL,
            headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
            data=json.dumps({
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            })
        )
        response_data = response.json()

        if "choices" in response_data and response_data["choices"]:
            ai_answer = response_data["choices"][0]["message"]["content"].strip()

            pdf_conversation_history.append({"role": "assistant", "content": ai_answer})

            return ai_answer
        else:
            return 'NO_INFO' 
    
    except Exception as e:
        return f"Error: {e}"


