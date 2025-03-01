import tkinter as tk
from tkinter import messagebox
from openai import OpenAI
import requests
from PIL import Image, ImageTk
from io import BytesIO

# Initialize OpenAI client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",  # Replace with your OpenRouter API key
)

# Function to fetch image from URL and display response
def fetch_image_url():
    url = url_entry.get()
    
    if not url:
        messagebox.showwarning("Input Error", "Please enter an image URL!")
        return

    try:
        # Make a request to the Gemini model
        completion = client.chat.completions.create(
            extra_headers={},
            extra_body={},
            model="google/gemini-2.0-pro-exp-02-05:free",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "What is in this image?"},
                        {"type": "image_url", "image_url": {"url": url}},
                    ]
                }
            ]
        )
        
        # Get response content
        response_content = completion.choices[0].message.content.strip()

        # Display response in the label
        response_label.config(text="AI Response: " + response_content)

        # Display image in window
        try:
            response = requests.get(url)
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            img = img.resize((250, 250))  # Resize the image to fit the window
            img = ImageTk.PhotoImage(img)
            img_label.config(image=img)
            img_label.image = img
        except Exception as e:
            messagebox.showerror("Error", "Failed to load image. Check the URL.")

    except Exception as e:
        messagebox.showerror("API Error", f"Error with API call: {str(e)}")

# Set up the GUI window
root = tk.Tk()
root.title("AI Image Description")

# Input field for image URL
url_label = tk.Label(root, text="Enter Image URL:")
url_label.pack(pady=5)

url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Button to fetch image and description
fetch_button = tk.Button(root, text="Fetch Image Description", command=fetch_image_url)
fetch_button.pack(pady=10)

# Label to display the AI's response
response_label = tk.Label(root, text="AI Response: ", wraplength=400)
response_label.pack(pady=10)

# Label to display the image
img_label = tk.Label(root)
img_label.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
