from pypdf import PdfReader
from docx import Document
import re

class CvExtractionService:

    def extract_cv_text(self, file_path, file_type):
        if file_type == 'pdf':
            return self.extract_pdf(file_path)
        elif file_type == 'docx':
            return self.extract_docx(file_path)
        else:
            return self.extract_text(file_path)

    def extract_pdf(self, pdf_path):
        text = ""
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
               
        return self.clean_text(text)

    def extract_docx(self, docx_path):
        doc = Document(docx_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return self.clean_text(text)

    def clean_text(self, text):
        # Remove extra whitespace, normalize line breaks
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # Remove non-ASCII
        return text.strip()

    def extract_text(self, text):
        pass



