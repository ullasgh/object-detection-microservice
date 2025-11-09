# 🧠 Object Detection Microservice (Python 3.11 + YOLOv3-tiny)
Detects objects in uploaded images, outputs annotated images and JSON results.
## Run
cd ai-backend; python -m venv venv; .\venv\Scripts\activate; pip install -r requirements.txt; python app.py
cd ui-backend; python -m venv venv; .\venv\Scripts\activate; pip install -r requirements.txt; python app.py
## Test
curl.exe -X POST -F "image=@F:/PROJECTS/object-detection-microservice/test_images/sample.jpeg" http://127.0.0.1:5000/detect
Outputs stored in /outputs as .jpeg + .json
## Docker
docker-compose up --build
