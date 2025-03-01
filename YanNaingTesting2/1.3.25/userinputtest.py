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
