from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "spotdl worker is running"

@app.route("/download", methods=["POST"])
def download_song():
    data = request.json
    spotify_url = data.get("url")
    if not spotify_url:
        return jsonify({"error": "no url provided"}), 400

    os.makedirs("downloads", exist_ok=True)
    result = subprocess.run(
    ["spotdl", "download", spotify_url, "--output", "downloads",
     "--threads", "1", "--cookie-file", "/etc/secrets/cookies.txt"],
    capture_output=True, text=True
)

    return jsonify({
        "status": "done" if result.returncode == 0 else "error",
        "log": (result.stdout + result.stderr)[-500:]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))