from flask import Flask, request, jsonify
from func import email_classify, email_response

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Rodando"

@app.route("/classify", methods=["POST"])
def classify():
    data = request.get_json()

    if not data or "email" not in data:
        return jsonify({"error":"Precisa enviar um JSON com a chave 'email'"})
    
    email_text = data["email"]

    category = email_classify(email_text)
    response = email_response(category)

    result = {
        "categoria": category,
        "resposta": response,
    }

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)