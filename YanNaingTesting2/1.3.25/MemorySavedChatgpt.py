import pickle
import os
from openai import OpenAI

# File to store chat history
CHAT_HISTORY_FILE = "chat_history.pkl"

# Function to load chat history from file
def load_chat_history():
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, "rb") as file:
            return pickle.load(file)
    return []

# Function to save chat history to file
def save_chat_history(history):
    with open(CHAT_HISTORY_FILE, "wb") as file:
        pickle.dump(history, file)

# Initialize OpenAI client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)

# Load previous chat history
chat_history = load_chat_history()

print("Chatbot is ready! Type 'exit' to quit.\n")

while True:
    # Get user input
    user_input = input("You: ")

    # Exit condition
    if user_input.lower() == "exit":
        print("Goodbye! Your conversation is saved.")
        save_chat_history(chat_history)  # Save history before exiting
        break

    # Append user message to chat history
    chat_history.append({"role": "user", "content": user_input})

    # Send full chat history to model
    completion = client.chat.completions.create(
        extra_headers={},
        extra_body={},
        model="openai/gpt-3.5-turbo-instruct",
        messages=chat_history
    )

    # Get response and add it to history
    ai_response = completion.choices[0].message.content.strip()
    chat_history.append({"role": "assistant", "content": ai_response})

    # Save updated chat history
    save_chat_history(chat_history)

    # Display the response
    print("AI:", ai_response)
