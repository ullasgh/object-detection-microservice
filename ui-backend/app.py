from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import requests, os
from pathlib import Path

app = Flask(__name__)
app.config.update(UPLOAD_FOLDER="uploads", OUTPUT_FOLDER="outputs", MAX_CONTENT_LENGTH=16*1024*1024)
[Path(p).mkdir(exist_ok=True) for p in [app.config["UPLOAD_FOLDER"], app.config["OUTPUT_FOLDER"]]]

AI_URL = os.environ.get("AI_BACKEND_URL","http://ai-backend:5001")
ALLOWED = {"png","jpg","jpeg"}
def allowed(f): return "." in f and f.rsplit(".",1)[1].lower() in ALLOWED

@app.route("/health")
def health():
    try:
        r=requests.get(f"{AI_URL}/health",timeout=3)
        return jsonify({"ui":"ok","ai":r.json()}),200
    except Exception as e:
        return jsonify({"ui":"ok","ai":{"status":"down","error":str(e)}}),200

@app.route("/detect",methods=["POST"])
def detect():
    if "image" not in request.files: return jsonify({"error":"No image"}),400
    f=request.files["image"]
    if f.filename=="": return jsonify({"error":"Empty filename"}),400
    if not allowed(f.filename): return jsonify({"error":"Invalid file"}),400
    name=secure_filename(f.filename)
    up=os.path.join(app.config["UPLOAD_FOLDER"],name); f.save(up)
    with open(up,"rb") as img:
        r=requests.post(f"{AI_URL}/detect",files={"image":img},timeout=60)
    if r.status_code!=200: return jsonify({"error":"AI backend fail","details":r.text}),r.status_code
    data=r.json(); out=data.get("output_filename")
    if out:
        img_r=requests.get(f"{AI_URL}/output/{out}",timeout=60)
        if img_r.status_code==200:
            op=os.path.join(app.config["OUTPUT_FOLDER"],out)
            [byte]$bytes = $img_r.Content
            [System.IO.File]::WriteAllBytes($op,$bytes)
            data["output_url"]=f"/output/{out}"
    return jsonify(data),200

@app.route("/output/<f>")
def output(f):
    p=os.path.join(app.config["OUTPUT_FOLDER"],secure_filename(f))
    return send_file(p) if os.path.exists(p) else (jsonify({"error":"Not found"}),404)

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
