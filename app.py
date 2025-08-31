import os
from flask import Flask, request, jsonify, send_from_directory
from app.func import (
    allowed_file,
    extract_text_from_pdf,
    extract_text_from_txt,
    extract_text_from_eml,
    process_email_text,
)

app = Flask(__name__)

PAGE_DIR = os.path.join(os.path.dirname(__file__), "page")
PAGE_DIR = os.path.abspath(PAGE_DIR)

@app.route("/classify", methods=["POST"])
def classify():
    email_text = None

    if request.is_json:
        data = request.get_json()
        if data and "email" in data:
            email_text = data["email"]
    elif "email_text" in request.form:
        email_text = request.form["email_text"]

    if not email_text:
        return jsonify({"error": "Campo 'email' obrigatório"}), 400

    result = process_email_text(email_text)
    return jsonify(result)


@app.route("/classify-file", methods=["POST"])
def classify_file():
    if "file" not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    file = request.files["file"]
    if file.filename == "" or not allowed_file(file.filename):
        return jsonify({"error": "Tipo de arquivo não suportado"}), 400

    ext = file.filename.rsplit(".", 1)[1].lower()
    email_text = ""

    try:
        if ext == "pdf":
            email_text = extract_text_from_pdf(file)
        elif ext == "txt":
            email_text = extract_text_from_txt(file)
        elif ext == "eml":
            email_text = extract_text_from_eml(file)
        else:
            return jsonify({"error": "Extensão não suportada"}), 400
    except Exception as e:
        return jsonify({"error": f"Erro ao processar arquivo: {str(e)}"}), 500

    if not email_text:
        return jsonify({"error": "Não foi possível extrair conteúdo"}), 400

    result = process_email_text(email_text)
    return jsonify(result)


@app.route("/")
def index():
    return send_from_directory(PAGE_DIR, "index.html")


@app.route("/<path:path>")
def static_files(path):
    if path.startswith("classify"):
        return jsonify({"error": "Rota inválida"}), 404
    return send_from_directory(PAGE_DIR, path)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port, debug=False)