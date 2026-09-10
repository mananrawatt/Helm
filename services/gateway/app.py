from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "service": "gateway",
        "message": "Gateway microservice is running"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "gateway"
    })


@app.route("/gateway")
def gateway():
    return jsonify({
        "message": "Gateway endpoint is available"
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8090
    )
