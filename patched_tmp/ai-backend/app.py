from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
from pathlib import Path
from utils import load_yolo_model, detect_objects, draw_detections
import cv2

app = Flask(__name__)
app.config.update(
    UPLOAD_FOLDER="uploads",
    OUTPUT_FOLDER="outputs",
    MODEL_FOLDER="models",
    MAX_CONTENT_LENGTH=16 * 1024 * 1024
)
[Path(p).mkdir(exist_ok=True) for p in [app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER'], app.config['MODEL_FOLDER']]]

ALLOWED_EXT = {'png','jpg','jpeg'}
def allowed(f): return '.' in f and f.rsplit('.',1)[1].lower() in ALLOWED_EXT

# Try to load model, but don't crash if missing - we'll handle at detect time
try:
    net, classes, out_layers = load_yolo_model(app.config['MODEL_FOLDER'])
    app.logger.info("YOLO model loaded.")
except Exception as e:
    app.logger.warning(f"YOLO model not loaded at startup: {e}")
    net, classes, out_layers = None, None, None

@app.route('/health')
def health():
    # Always return JSON quickly so UI health checks don't hang.
    return jsonify({"status":"ok"}), 200

@app.route('/detect', methods=['POST'])
def detect():
    if net is None:
        return jsonify({'error':'Model not loaded'}), 503
    if 'image' not in request.files:
        return jsonify({'error':'No image'}),400
    f = request.files['image']
    if f.filename == '':
        return jsonify({'error':'Empty filename'}),400
    if not allowed(f.filename):
        return jsonify({'error':'Invalid type'}),400
    name = secure_filename(f.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], name); f.save(path)
    img = cv2.imread(path)
    if img is None: return jsonify({'error':'Read fail'}),400
    try:
        dets = detect_objects(net, out_layers, classes, img)
        out = draw_detections(img.copy(), dets)
        out_name = f"result_{name}"
        cv2.imwrite(os.path.join(app.config['OUTPUT_FOLDER'], out_name), out)
        return jsonify({'detections':dets,'output_filename':out_name}),200
    except Exception as e:
        app.logger.exception("Detection failed")
        return jsonify({'error':str(e)}),500

@app.route('/output/<fname>')
def get_out(fname):
    p=os.path.join(app.config['OUTPUT_FOLDER'],secure_filename(fname))
    return send_file(p) if os.path.exists(p) else (jsonify({'error':'Not found'}),404)

if __name__=='__main__':
    app.run(host='0.0.0.0',port=5001,debug=True)