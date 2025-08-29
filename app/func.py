import os
from flask import request, jsonify, send_from_directory
from services.classifier import email_classify
from werkzeug.utils import secure_filename
import PyPDF2
from PyPDF2 import PdfReader
import email

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
ALLOWED_EXTENSIONS = {"pdf", "eml", "msg", "txt"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_pdf(filepath):
    text = ""
    with open(filepath, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text.strip()

def extract_text_from_txt(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        return f.read().strip()

def extract_text_from_eml(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        msg = email.message_from_file(f)
    text = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                text += part.get_payload(decode=True).decode(errors="ignore")
    else:
        text = msg.get_payload(decode=True).decode(errors="ignore")
    return text.strip()


def routes(app):
    @app.route("/classify", methods=["POST"])
    def classify():
        data = request.get_json()
        
        email_text = None

        if request.is_json:
            data = request.get_json()
            if data and "email" in data:
                email_text = data["email"]
        
        elif "email_text" in request.form:
            email_text = request.form["email_text"]

        elif "email_file" in request.files:
            file = request.files["email_file"]
            if file.filename.endswith(".txt"):
                email_text = file.read().decode("utf-8")
            elif file.filename.endswith(".pdf"):
                reader = PdfReader(file)
                email_text = ""
                for page in reader.pages:
                    email_text += page.extract_text() + "\n"

        if not email_text:
            return jsonify({"error": "Campo 'email obrigatorio"}), 400
        
        category= email_classify(email_text)

        result = {
            "original_email": email_text,
            "category": category
        }

        return jsonify(result)
    
    @app.route("/classify-file", methods=["POST"])
    def classify_file():
        if "file" not in request.files:
            return jsonify({"error": "Erro"})
        
        file = request.files["file"]

        if file.filename == "" or not allowed_file(file.filename):
            return jsonify({"error":"Tipo nao suportado"}), 400
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        ext = filename.rsplit(".", 1)[1].lower()
        email_text = ""
        try:
            if ext == "pdf":
                email_text = extract_text_from_pdf(filepath)
            elif ext == "txt":
                email_text = extract_text_from_txt(filepath)
            elif ext == "eml":
                email_text = extract_text_from_eml(filepath)
            else:
                return jsonify({"error":"extensão não suportada"}), 400
        except Exception as e:
            return jsonify({"error":f"Erro ao processar arquivo: {str(e)}"}), 500
        if not email_text:
            return jsonify({"error":"Não é possivel extrair arquivo"}), 400
        category = email_classify(email_text)
        result = {
            "original_email": email_text[:500] + ". . .",
            "category": category
        }
        return jsonify(result)
    @app.route("/")
    def index():
        return send_from_directory(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), "page"), "index.html")

    @app.route("/<path:path>")
    def static_files(path):
        return send_from_directory(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), "page"), path)