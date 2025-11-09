from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import cv2
import numpy as np
import os
from pathlib import Path
from utils import load_yolo_model, detect_objects, draw_detections

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['MODEL_FOLDER'] = 'models'

Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)
Path(app.config['OUTPUT_FOLDER']).mkdir(exist_ok=True)

print("Loading YOLO model...")
net, classes, output_layers = load_yolo_model(app.config['MODEL_FOLDER'])
print("YOLO model loaded successfully!")

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'ai-backend'}), 200

@app.route('/detect', methods=['POST'])
def detect():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        image = cv2.imread(filepath)
        if image is None:
            return jsonify({'error': 'Failed to read image'}), 400
        
        detections = detect_objects(image, net, classes, output_layers)
        
        output_image = draw_detections(image.copy(), detections)
        
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        cv2.imwrite(output_path, output_image)
        
        response = {
            'success': True,
            'image_name': filename,
            'total_objects': len(detections),
            'detections': detections
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': f'Detection failed: {str(e)}'}), 500

@app.route('/output/<filename>', methods=['GET'])
def get_output(filename):
    try:
        filepath = os.path.join(app.config['OUTPUT_FOLDER'], secure_filename(filename))
        if os.path.exists(filepath):
            return send_file(filepath, mimetype='image/jpeg')
        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
