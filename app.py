from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__)
CORS(app)

DOWNLOAD_DIR = "downloads"

@app.route("/")
def home():
    return "spotdl worker is running"

@app.route("/download", methods=["POST"])
def download_song():
    data = request.json
    spotify_url = data.get("url")
    if not spotify_url:
        return jsonify({"error": "no url provided"}), 400

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    result = subprocess.run(
        ["spotdl", "download", spotify_url, "--output", DOWNLOAD_DIR, "--threads", "2"],
        capture_output=True, text=True
    )

    return jsonify({
        "status": "done" if result.returncode == 0 else "error",
        "log": (result.stdout + result.stderr)[-1000:]
    })

@app.route("/files", methods=["GET"])
def list_files():
    files = os.listdir(DOWNLOAD_DIR) if os.path.exists(DOWNLOAD_DIR) else []
    return jsonify([{"name": f, "url": f"/files/{f}"} for f in files])

@app.route("/files/<path:filename>", methods=["GET"])
def get_file(filename):
    return send_from_directory(DOWNLOAD_DIR, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), threaded=True)