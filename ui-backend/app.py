from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import requests
import os
import json
from pathlib import Path

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)
Path(app.config['OUTPUT_FOLDER']).mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
AI_BACKEND_URL = 'http://ai-backend:5001'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'ui-backend'}), 200

@app.route('/detect', methods=['POST'])
def detect_objects():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed: png, jpg, jpeg'}), 400
    
    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        with open(filepath, 'rb') as img:
            files = {'image': (filename, img, 'image/jpeg')}
            response = requests.post(f'{AI_BACKEND_URL}/detect', files=files, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            
            json_filename = f"{os.path.splitext(filename)[0]}_detection.json"
            json_path = os.path.join(app.config['OUTPUT_FOLDER'], json_filename)
            with open(json_path, 'w') as f:
                json.dump(result, f, indent=2)
            
            img_response = requests.get(f'{AI_BACKEND_URL}/output/{filename}', timeout=30)
            if img_response.status_code == 200:
                output_img_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
                with open(output_img_path, 'wb') as f:
                    f.write(img_response.content)
            
            return jsonify({
                'success': True,
                'detections': result['detections'],
                'total_objects': result['total_objects'],
                'image_output': f'/output/{filename}',
                'json_output': f'/output/{json_filename}'
            }), 200
        else:
            return jsonify({'error': 'AI backend processing failed'}), 500
            
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Communication error with AI backend: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Processing error: {str(e)}'}), 500

@app.route('/output/<filename>', methods=['GET'])
def get_output(filename):
    try:
        filepath = os.path.join(app.config['OUTPUT_FOLDER'], secure_filename(filename))
        if os.path.exists(filepath):
            return send_file(filepath)
        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
