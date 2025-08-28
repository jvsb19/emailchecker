from flask import request, jsonify
from services.classifier import email_classify

def routes(app):
    @app.route("/classify", methods=["POST"])
    def classify():
        data = request.get_json()

        if not data or "email" not in data:
            return jsonify({"error": "Campo 'email obrigatorio"}), 400
        
        email_text = data["email"]
        
        category= email_classify(email_text)

        result = {
            "original_email": email_text,
            "category": category
        }

        return jsonify(result)
        