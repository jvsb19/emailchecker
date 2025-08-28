from flask import Flask, request, jsonify
from func import routes

def run_app():
    app = Flask(__name__)
    routes(app)
    return app

if __name__ == "__main__":
    app = run_app()
    app.run(debug=True)