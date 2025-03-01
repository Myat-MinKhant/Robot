import tkinter as tk
from tkinter import scrolledtext, messagebox
from datetime import datetime
import os
import pickle
from openai import OpenAI
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# Initialize OpenAI client for OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",  # Replace with your API key
)

# Initialize the translation pipeline
checkpoint = "facebook/nllb-200-distilled-600M"
model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)
tokenizer = AutoTokenizer.from_pretrained(checkpoint)

# Translation function with chunking for long texts
def translate(text, src_lang="mya_Mymr", tgt_lang="eng_Latn"):
    try:
        translator = pipeline('translation', model=model, tokenizer=tokenizer, src_lang=src_lang, tgt_lang=tgt_lang, max_length=400, device=0)  # Use GPU
        # Split long text into chunks for better translation
        chunks = [text[i:i + 200] for i in range(0, len(text), 200)]
        translated_chunks = []
        for chunk in chunks:
            output = translator(chunk)
            translated_chunks.append(output[0]["translation_text"])
        return " ".join(translated_chunks)
    except Exception as e:
        raise Exception(f"Translation error: {str(e)}")

class ChatbotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Chatbot - Burmese & English")
        self.root.geometry("800x600")
        self.root.configure(bg="#2E3440")  # Dark background for modern look

        self.chat_history = []
        self.load_chat_history()

        # Main Chat Frame
        self.main_frame = tk.Frame(root, bg="#2E3440")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Chat Area
        self.chat_area = scrolledtext.ScrolledText(
            self.main_frame, height=20, width=70, wrap=tk.WORD, state=tk.DISABLED,
            bg="#3B4252", fg="#ECEFF4", font=("Arial", 12), insertbackground="white"
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Sidebar Frame
        self.sidebar_frame = tk.Frame(root, width=200, bg="#4C566A")
        self.sidebar_frame.pack(fill=tk.Y, side=tk.LEFT, padx=10, pady=10)

        self.sidebar_label = tk.Label(self.sidebar_frame, text="Chat History", bg="#4C566A", fg="#ECEFF4", font=("Arial", 14, "bold"))
        self.sidebar_label.pack(pady=10)

        self.sidebar = tk.Listbox(
            self.sidebar_frame, width=25, bg="#4C566A", fg="#ECEFF4", font=("Arial", 10),
            selectbackground="#81A1C1", selectforeground="#2E3440"
        )
        self.sidebar.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Entry Frame
        self.entry_frame = tk.Frame(root, bg="#2E3440")
        self.entry_frame.pack(fill=tk.X, padx=10, pady=10)

        self.entry = tk.Entry(
            self.entry_frame, width=50, font=("Arial", 12), bg="#4C566A", fg="#ECEFF4",
            insertbackground="white"
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        self.send_button = tk.Button(
            self.entry_frame, text="Send", command=self.send_message, font=("Arial", 12),
            bg="#81A1C1", fg="#2E3440", activebackground="#88C0D0", activeforeground="#2E3440"
        )
        self.send_button.pack(side=tk.LEFT)

        # Exit Button
        self.quit_button = tk.Button(
            root, text="Exit", command=self.exit_chat, font=("Arial", 12),
            bg="#BF616A", fg="#ECEFF4", activebackground="#D08770", activeforeground="#2E3440"
        )
        self.quit_button.pack(pady=10)

        # Bind Enter key to send message
        self.entry.bind("<Return>", lambda event: self.send_message())

        self.update_sidebar()
        self.update_chat_area()

    def send_message(self):
        user_input = self.entry.get()
        if user_input.strip():
            # Translate Burmese input to English
            try:
                english_input = translate(user_input, src_lang="mya_Mymr", tgt_lang="eng_Latn")
            except Exception as e:
                messagebox.showerror("Translation Error", f"Failed to translate input: {str(e)}")
                return

            # Add original Burmese input and translated English input to chat history
            self.chat_history.append({"role": "user", "content": user_input, "translated_content": english_input, "date": datetime.now()})
            self.update_chat_area()
            self.entry.delete(0, tk.END)
            self.respond(english_input)
            self.save_chat_history()

    def respond(self, english_input):
        # Prepare the messages for the API (remove non-serializable datetime objects)
        api_messages = [
            {"role": msg["role"], "content": msg["translated_content"] if "translated_content" in msg else msg["content"]}
            for msg in self.chat_history
        ]

        # Send the English input to the DeepSeek model via OpenRouter
        try:
            completion = client.chat.completions.create(
                extra_headers={},
                extra_body={},
                model="deepseek/deepseek-r1-distill-llama-70b:free",  # Using the DeepSeek model
                messages=api_messages  # Send the cleaned conversation history
            )

            # Get AI response in English
            english_response = completion.choices[0].message.content.strip()

            # Translate the AI's English response back to Burmese
            try:
                burmese_response = translate(english_response, src_lang="eng_Latn", tgt_lang="mya_Mymr")
            except Exception as e:
                messagebox.showerror("Translation Error", f"Failed to translate AI response: {str(e)}")
                return

            # Add AI response to chat history
            self.chat_history.append({"role": "assistant", "content": burmese_response, "translated_content": english_response, "date": datetime.now()})
            self.update_chat_area()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get AI response: {str(e)}")

    def update_chat_area(self):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.delete(1.0, tk.END)

        for msg in self.chat_history[-10:]:  # Show the latest 10 messages
            date = msg["date"].strftime("%Y-%m-%d %H:%M:%S")
            role = "You: " if msg["role"] == "user" else "AI: "
            content = msg["content"]  # Display in Burmese for user
            self.chat_area.insert(tk.END, f"[{date}] {role} {content}\n\n")

        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.yview(tk.END)  # Auto-scroll to the bottom

    def update_sidebar(self):
        self.sidebar.delete(0, tk.END)
        for msg in self.chat_history:
            date = msg["date"].strftime("%Y-%m-%d %H:%M:%S")
            self.sidebar.insert(tk.END, f"{date} - {msg['content'][:30]}...")

    def load_chat_history(self):
        if os.path.exists("conversation_history.pkl"):
            with open("conversation_history.pkl", "rb") as file:
                self.chat_history = pickle.load(file)

            # Ensure that each message has a date
            for msg in self.chat_history:
                if "date" not in msg:
                    msg["date"] = datetime.now()

    def save_chat_history(self):
        with open("conversation_history.pkl", "wb") as file:
            pickle.dump(self.chat_history, file)

    def exit_chat(self):
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.save_chat_history()
            self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotApp(root)
    root.mainloop()