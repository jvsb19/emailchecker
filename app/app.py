from flask import Flask, request, jsonify
from .func import routes

app = Flask(__name__)
routes(app)

if __name__ == "__main__":
    app.run(debug=True)