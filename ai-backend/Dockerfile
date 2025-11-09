FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    wget \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p uploads outputs models

RUN cd models && \
    wget -q https://pjreddie.com/media/files/yolov3.weights && \
    wget -q https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg && \
    wget -q https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names

EXPOSE 5001

CMD ["python", "app.py"]
