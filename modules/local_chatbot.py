import google.generativeai as genai
from pypdf import PdfReader

# Define file path
pdf_path = ''

try:
    # Creating a pdf reader object
    reader = PdfReader(pdf_path)

    # Printing number of pages in the PDF file
    print(f"Total Pages: {len(reader.pages)}")

    # Extracting text from the first two pages (if they exist)
    text = reader.pages[0].extract_text() if len(reader.pages) > 0 else "No text found"
    text1 = reader.pages[1].extract_text() if len(reader.pages) > 1 else "No second page"

    # Printing extracted text
    print(f"This is the sample text:\n{text}\n{text1}")

except FileNotFoundError:
    print("Error: The PDF file was not found. Please check the file path.")
except Exception as e:
    print(f"An error occurred: {e}")

# Set up Gemini API key
genai.configure(api_key="AIzaSyDo01CBIaanACl5voE9NEm7CdjtFPp6P2c")

# Load extracted text from file
def load_text(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print("Error: Text file not found.")
        return ""

# Generate AI response using Gemini
def get_gemini_response(query, context):
    prompt = f"Based on the following document:\n\n{context}\n\nAnswer the question: {query}"

    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text  # Extract response text
    except Exception as e:
        return f"Error: {e}"

# Chatbot function
def chatbot():
    pdf_text = load_text("/home/pi/Desktop/Robot/resources/pdf_files/ameca.text")

    if not pdf_text:
        print("No data available for chatbot.")
        return

    print("Gemini AI Chatbot is ready! Type 'exit' to quit.")

    while True:
        user_input = input("\nYou: ")

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        response = get_gemini_response(user_input, pdf_text)
        print(f"Chatbot: {response}")

# Run chatbot
chatbot()