from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "service": "tags",
        "message": "Tags microservice is running"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "tags"
    })


@app.route("/tags")
def tags():
    return jsonify({
        "message": "Tags endpoint is available"
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8089
    )
