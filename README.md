# 🧠 Object Detection Microservice (Python 3.11 + YOLOv3-tiny)

This microservice detects objects in uploaded images using YOLOv3-tiny, returning both:
- ✅ Annotated image with bounding boxes
- ✅ JSON file containing detections

---

## 🚀 Tech Stack
- **Python:** 3.11
- **Framework:** Flask
- **Libraries:** OpenCV, NumPy, Requests
- **Deployment:** Docker + Docker Compose

---

## ⚙️ Manual Run
### Start AI backend
cd ai-backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python app.py

### Start UI backend (new terminal)
cd ui-backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python app.py

---

## ✅ Test Health
Invoke-WebRequest -Uri "http://127.0.0.1:5000/health"

Response:
{
  "ui": "ok",
  "ai": { "status": "ok" }
}

---

## 🧪 Object Detection Example
curl.exe -X POST -F "image=@F:/PROJECTS/object-detection-microservice/test_images/sample.jpeg" http://127.0.0.1:5000/detect

Result:
{
  "detections": [
    { "class": "dog", "confidence": 0.99 }
  ],
  "output_url": "/output/result_sample.jpeg",
  "output_json_url": "/output/result_sample.json"
}

Both files are stored in:
outputs/
├── result_sample.jpeg
└── result_sample.json

---

## 🐳 Docker Run
docker-compose up --build

Then open: http://127.0.0.1:5000

---

## 🧼 Cleanup
git clean -fdx

---

Built and debugged by **Ullas G H**
