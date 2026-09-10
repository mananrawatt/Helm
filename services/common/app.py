from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "service": "common",
        "message": "Common microservice is running"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "common"
    })


@app.route("/common")
def common():
    return jsonify({
        "message": "Common endpoint is available"
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8088
    )
