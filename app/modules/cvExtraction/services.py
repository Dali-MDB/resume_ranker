from pypdf import PdfReader
from docx import Document
import re
from app.utils.file_utils import extract_docx, extract_pdf, extract_text

class CvExtractionService:

    def extract_cv_text(self, file_path, file_type):
        if file_type == 'pdf':
            return extract_pdf(file_path)
        elif file_type == 'docx':
            return extract_docx(file_path)
        else:
            return extract_text(file_path)

    def extract_pdf_text(self, pdf_path):
        return extract_pdf(pdf_path)

    def extract_docx_text(self, docx_path):
        return extract_docx(docx_path)

    def extract_text_text(self, text):
        return extract_text(text)


