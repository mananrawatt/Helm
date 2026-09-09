from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "service": "payments",
        "message": "Payments microservice is running"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "payments"
    })


@app.route("/payments")
def payments():
    return jsonify({
        "message": "Payments endpoint is available"
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8087
    )
