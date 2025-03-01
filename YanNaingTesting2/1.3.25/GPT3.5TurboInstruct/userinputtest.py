from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)

# Chat history to maintain context
chat_history = []

print("Chatbot is ready! Type 'exit' to quit.\n")

while True:
    # Get user input
    user_input = input("You: ")
    
    # Exit condition
    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    # Append user message to chat history
    chat_history.append({"role": "user", "content": user_input})

    # Send full chat history to model
    completion = client.chat.completions.create(
        extra_headers={},
        extra_body={},
        model="openai/gpt-3.5-turbo-instruct",
        messages=chat_history  # Send conversation history
    )

    # Get response and add it to history
    ai_response = completion.choices[0].message.content.strip()
    chat_history.append({"role": "assistant", "content": ai_response})

    # Display the response
    print("AI:", ai_response)
