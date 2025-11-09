# 🧠 Object Detection Microservice (Python 3.11 + YOLOv3-tiny)

A two-tier Flask microservice for object detection using YOLOv3-tiny, built for clarity and containerized for deployment.

---

## 🚀 Tech Stack
- **Language:** Python 3.11
- **Framework:** Flask
- **Libraries:** OpenCV, NumPy, Requests
- **Model:** YOLOv3-tiny
- **Deployment:** Docker + Docker Compose

---

## 📁 Project Structure
ai-backend/ → YOLO model inference service (port 5001)
ui-backend/ → File upload + routing frontend (port 5000)
models/ → Pre-trained YOLO model files (.weights, .cfg)
test_images/ → Sample input images

---

## 🧩 Setup (Manual Run)
### 1️⃣ Create & activate virtual environments
cd ai-backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python app.py

# In another terminal:
cd ui-backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python app.py

---

## 🧪 Test Health
Invoke-WebRequest -Uri "http://127.0.0.1:5000/health"

Response:
{
  "ui": "ok",
  "ai": { "status": "ok" }
}

---

## 📸 Object Detection
curl.exe -X POST -F "image=@F:/PROJECTS/object-detection-microservice/test_images/sample.jpeg" http://127.0.0.1:5000/detect

Result:
{
  "detections": [
    { "class": "dog", "confidence": 0.99 }
  ],
  "output_url": "/output/result_sample.jpeg"
}

Open: http://127.0.0.1:5000/output/result_sample.jpeg

---

## 🐳 Run with Docker
docker-compose up --build

Then open: http://127.0.0.1:5000

---

## 🧼 Cleanup
git clean -fdx

---

## 🏁 Credits
Built and debugged by **Ullas G H** — YOLO-powered Flask microservice architecture with AI + backend integration.
