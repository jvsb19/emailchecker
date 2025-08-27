import email
from PyPDF2 import PdfReader
from app.services.classifier import email_classify, email_response
from app.services.nlp_utils import preprocess_text

ALLOWED_EXTENSIONS = {"pdf", "eml", "msg", "txt"}

def allowed_file(filename: str) -> bool:
    """Verifica se o arquivo tem extensão válida"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_pdf(file) -> str:
    """Extrai texto de PDF"""
    text = ""
    reader = PdfReader(file)
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.strip()


def extract_text_from_txt(file) -> str:
    """Extrai texto de TXT"""
    return file.read().decode("utf-8", errors="ignore").strip()


def extract_text_from_eml(file) -> str:
    """Extrai texto de EML"""
    msg = email.message_from_bytes(file.read())
    text = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                text += part.get_payload(decode=True).decode(errors="ignore")
    else:
        text = msg.get_payload(decode=True).decode(errors="ignore")
    return text.strip()


def process_email_text(email_text: str) -> dict:
    """Classifica um texto de e-mail simples"""
    processText = preprocess_text(email_text)
    processText = " ".join(processText)
    category = email_classify(processText)
    response = email_response(category)

    return {
        "original_email": email_text[:500] + "..." if len(email_text) > 500 else email_text,
        "category": category,
        "response": response,
    }

