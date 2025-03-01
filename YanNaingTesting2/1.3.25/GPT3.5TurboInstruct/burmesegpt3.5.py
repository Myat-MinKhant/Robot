##Not working very well!!
import pickle
import os
from openai import OpenAI
import sys
sys.stdout.reconfigure(encoding='utf-8')


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

print("🤖 Chatbot is ready! (Supports Burmese & English) | Type 'exit' to quit.\n")

while True:
    # Get user input (Supports Burmese & English)
    user_input = input("You: ")

    # Exit condition
    if user_input.lower() == "exit":
        print("📁 Conversation saved. Goodbye!")
        save_chat_history(chat_history)  # Save before exiting
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

    # Get AI response and store it
    ai_response = completion.choices[0].message.content.strip()
    chat_history.append({"role": "assistant", "content": ai_response})

    # Save updated chat history
    save_chat_history(chat_history)

    # Display the response
    print("AI:", ai_response)
