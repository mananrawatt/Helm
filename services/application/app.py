from flask import Flask, jsonify
import os

app = Flask(__name__)

APP_PORT = 8085


@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to the Helm Learning Application!",
        "version": os.getenv("APP_VERSION", "1.0.0")
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    }), 200


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=APP_PORT
    )