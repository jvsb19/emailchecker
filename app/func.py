import email
from PyPDF2 import PdfReader
from app.services.classifier import email_classify, email_response
from app.services.nlp_utils import preprocess_text

ALLOWED_EXTENSIONS = {"pdf", "msg", "txt"}


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_pdf(file) -> str:
    
    text = ""
    reader = PdfReader(file)
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.strip()

def extract_text_from_txt(file) -> str:
    return file.read().decode("utf-8", errors="ignore").strip()

def process_email_text(email_text: str) -> dict:
    processText = preprocess_text(email_text)
    processText = " ".join(processText)
    category = email_classify(processText)
    response = email_response(category)

    return {
        "original_email": email_text[:500] + "..." if len(email_text) > 500 else email_text,
        "category": category,
        "response": response,
    }
