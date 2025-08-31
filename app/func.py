import os
from app.services.classifier import email_classify, email_response
from app.services.nlp_utils import preprocess_text
from PyPDF2 import PdfReader
import email

ALLOWED_EXTENSIONS = {"pdf", "eml", "msg", "txt"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_pdf(path):
    text = ""
    reader = PdfReader(path)
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.strip()


def extract_text_from_txt(path):
    with open(path, "rb") as f:
        return f.read().decode("utf-8", errors="ignore").strip()


def extract_text_from_eml(path):
    with open(path, "rb") as f:
        msg = email.message_from_bytes(f.read())
    text = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                text += part.get_payload(decode=True).decode(errors="ignore")
    else:
        text = msg.get_payload(decode=True).decode(errors="ignore")
    return text.strip()


def classify_text(email_text):
    if not email_text:
        return {"error": "Campo 'email' obrigatório"}

    processText = preprocess_text(email_text)
    processText = " ".join(processText)
    category = email_classify(processText)
    response = email_response(category)

    result = {
        "original_email": email_text[:500] + "..." if len(email_text) > 500 else email_text,
        "category": category,
        "response": response,
    }
    return result


def classify_file(path):
    filename = os.path.basename(path)  # pega só o nome do arquivo
    if not allowed_file(filename):
        return {"error": "Tipo de arquivo não suportado"}

    ext = path.rsplit(".", 1)[1].lower()
    email_text = ""

    try:
        if ext == "pdf":
            email_text = extract_text_from_pdf(path)
        elif ext == "txt":
            email_text = extract_text_from_txt(path)
        elif ext == "eml":
            email_text = extract_text_from_eml(path)
        else:
            return {"error": "Extensão não suportada"}
    except Exception as e:
        return {"error": f"Erro ao processar arquivo: {str(e)}"}

    if not email_text:
        return {"error": "Não foi possível extrair conteúdo"}

    processText = preprocess_text(email_text)
    processText = " ".join(processText)
    category = email_classify(processText)
    response = email_response(category)

    result = {
        "original_email": email_text[:500] + "..." if len(email_text) > 500 else email_text,
        "category": category,
        "response": response,
    }
    return result