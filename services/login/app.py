from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "service": "login",
        "message": "Login microservice is running"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "login"
    })


@app.route("/login")
def login():
    return jsonify({
        "message": "Login endpoint is available"
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8086
    )