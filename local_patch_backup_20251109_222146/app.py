from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import requests
import os
from pathlib import Path

app = Flask(__name__)
app.config.update(
    UPLOAD_FOLDER="uploads",
    OUTPUT_FOLDER="outputs",
    MAX_CONTENT_LENGTH=16 * 1024 * 1024
)

# Create folders if missing
[Path(p).mkdir(exist_ok=True) for p in [app.config["UPLOAD_FOLDER"], app.config["OUTPUT_FOLDER"]]]

# URL of the AI backend
AI_URL = os.environ.get("AI_BACKEND_URL", "http://127.0.0.1:5001")

ALLOWED = {"png", "jpg", "jpeg"}

def allowed(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED

@app.route("/health")
def health():
    """Health check for UI and AI backend"""
    try:
        r = requests.get(f"{AI_URL}/health", timeout=10)
        return jsonify({"ui": "ok", "ai": r.json()}), 200
    except Exception as e:
        return jsonify({"ui": "ok", "ai": {"status": "down", "error": str(e)}}), 200

@app.route("/detect", methods=["POST"])
def detect():
    """Upload image, send to AI backend, and return detections"""
    if "image" not in request.files:
        return jsonify({"error": "No image"}), 400

    f = request.files["image"]
    if f.filename == "":
        return jsonify({"error": "Empty filename"}), 400
    if not allowed(f.filename):
        return jsonify({"error": "Invalid file type"}), 400

    name = secure_filename(f.filename)
    upload_path = os.path.join(app.config["UPLOAD_FOLDER"], name)
    f.save(upload_path)

    try:
        # Send to AI backend
        with open(upload_path, "rb") as img_file:
            r = requests.post(f"{AI_URL}/detect", files={"image": img_file}, timeout=60)

        if r.status_code != 200:
            return jsonify({"error": "AI backend failed", "details": r.text}), r.status_code

        data = r.json()
        out = data.get("output_filename")

        # Fetch and save result image from AI backend
        if out:
            img_r = requests.get(f"{AI_URL}/output/{out}", timeout=60)
            if img_r.status_code == 200:
                output_path = os.path.join(app.config["OUTPUT_FOLDER"], out)
                with open(output_path, "wb") as f:
                    f.write(img_r.content)
                data["output_url"] = f"/output/{out}"

        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/output/<filename>")
def output(filename):
    """Serve processed image"""
    path = os.path.join(app.config["OUTPUT_FOLDER"], secure_filename(filename))
    return send_file(path) if os.path.exists(path) else (jsonify({"error": "Not found"}), 404)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

