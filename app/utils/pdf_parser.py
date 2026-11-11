# app/utils/pdf_parser.py
from PyPDF2 import PdfReader

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts and concatenates text from all pages of a PDF file.
    """
    text = ""
    with open(file_path, "rb") as f:
        reader = PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text.strip()
