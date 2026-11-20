from flask import Flask, jsonify, request
from flask_cors import CORS
from main_2 import run_pipeline

app = Flask(__name__)
CORS(app)


@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.get_json(silent=True) or {}
    query = data.get("query", "")

    print(f"受信した入力: {query}", flush=True)
    run_pipeline(query)

    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(port=5000, debug=True)