import fitz
from transformers import pipeline

class PDFQuestionAnswering:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.texts = self.extract_text_from_pdf()
        self.question_answerer = pipeline("question-answering", model="distilbert-base-cased-distilled-squad", tokenizer="distilbert-base-cased-distilled-squad")

    def extract_text_from_pdf(self):
        doc = fitz.open(self.pdf_path)
        text = ''
        for page_num in range(doc.page_count):
            page = doc[page_num]
            text += page.get_text()
        return text

    def answer_question(self, question):
        return self.question_answerer(context=self.texts, question=question)["answer"]

def main():
    pdf_path = 'mechatronics.pdf'  # Replace with the path to your PDF file
    pdf_qa = PDFQuestionAnswering(pdf_path)

    while True:
        user_question = input("Ask a question (type 'exit' to quit): ")
        if user_question.lower() == 'exit':
            break

        answer = pdf_qa.answer_question(user_question)
        print(f"Answer: {answer}")

if __name__ == "__main__":
    main()
