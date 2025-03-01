import pickle
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",  # Replace with your API key
)

# Load conversation history from file (if exists)
def load_conversation_history():
    try:
        with open("conversation_history.pkl", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return []  # Return an empty list if the file does not exist

# Save conversation history to file
def save_conversation_history(history):
    with open("conversation_history.pkl", "wb") as f:
        pickle.dump(history, f)

# Get user input
def get_user_input():
    return input("You: ")

# Main chat loop
def chat():
    conversation_history = load_conversation_history()  # Load past conversation history
    print("Chatbot is ready! Type 'exit' to quit.")
    
    while True:
        # Get user input
        user_message = get_user_input()
        
        if user_message.lower() == "exit":
            print("Exiting chat. Goodbye!")
            break

        # Add user message to conversation history
        conversation_history.append({"role": "user", "content": user_message})

        # Make a request to the model with the updated conversation history
        completion = client.chat.completions.create(
            extra_headers={},
            extra_body={},
            model="deepseek/deepseek-r1-distill-llama-70b:free",  # Using the model you specified
            messages=conversation_history  # Send the full conversation history
        )

        # Get AI response
        ai_response = completion.choices[0].message.content.strip()

        # Print AI response
        print(f"AI: {ai_response}")

        # Add AI response to conversation history
        conversation_history.append({"role": "assistant", "content": ai_response})

        # Save updated conversation history
        save_conversation_history(conversation_history)

# Start the chat
if __name__ == "__main__":
    chat()
