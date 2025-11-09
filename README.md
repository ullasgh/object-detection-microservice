# Object Detection Microservice System

A production-ready microservice system for object detection using YOLOv3, built with Flask and Docker.

## 🏗️ Architecture

\\\
┌─────────────┐         ┌─────────────┐
│   Client    │────────▶│ UI Backend  │
│             │         │   (Flask)   │
└─────────────┘         │  Port: 5000 │
                        └──────┬──────┘
                               │
                          HTTP POST
                               │
                        ┌──────▼──────┐
                        │ AI Backend  │
                        │   (Flask)   │
                        │  Port: 5001 │
                        │   + YOLOv3  │
                        └─────────────┘
\\\

## ✨ Features

- **Microservice Architecture**: Separated UI and AI backends for scalability
- **Object Detection**: YOLOv3 with COCO dataset (80 object classes)
- **RESTful API**: Clean, documented endpoints
- **Docker Ready**: Full containerization with Docker Compose
- **CPU Compatible**: No GPU required
- **JSON Output**: Structured detection results with confidence scores
- **Visual Output**: Images with bounding boxes and labels

## 🚀 Quick Start

### Prerequisites

- Docker (version 20.10+)
- Docker Compose (version 1.29+)
- 4GB+ RAM recommended

### Installation & Running

\\\ash
# 1. Clone the repository
git clone https://github.com/ullasgh/object-detection-microservice.git
cd object-detection-microservice

# 2. Build and start services
docker-compose up --build

# Wait for YOLO model to download (~250MB, first time only)
# Look for: "YOLO model loaded successfully!"
\\\

### Testing

\\\ash
# 1. Check health endpoints
curl http://localhost:5000/health
curl http://localhost:5001/health

# 2. Detect objects in an image
curl -X POST -F "image=@path/to/your/image.jpg" http://localhost:5000/detect

# 3. View outputs
# - Images with bounding boxes: ui-backend/outputs/
# - JSON detection results: ui-backend/outputs/
\\\

## 📡 API Documentation

### UI Backend API (Port 5000)

#### POST /detect
Upload an image for object detection.

**Request:**
\\\ash
curl -X POST -F "image=@image.jpg" http://localhost:5000/detect
\\\

**Response:**
\\\json
{
  "success": true,
  "detections": [
    {
      "class": "person",
      "confidence": 0.9856,
      "bounding_box": {
        "x": 100,
        "y": 150,
        "width": 200,
        "height": 400
      }
    },
    {
      "class": "car",
      "confidence": 0.8932,
      "bounding_box": {
        "x": 300,
        "y": 200,
        "width": 150,
        "height": 100
      }
    }
  ],
  "total_objects": 2,
  "image_output": "/output/image.jpg",
  "json_output": "/output/image_detection.json"
}
\\\

#### GET /output/{filename}
Retrieve processed image or JSON file.

\\\ash
curl http://localhost:5000/output/image.jpg --output result.jpg
curl http://localhost:5000/output/image_detection.json
\\\

#### GET /health
Health check endpoint.

\\\ash
curl http://localhost:5000/health
# Response: {"status": "healthy", "service": "ui-backend"}
\\\

## 📁 Project Structure

\\\
object-detection-microservice/
├── docker-compose.yml          # Multi-container orchestration
├── README.md                   # This file
├── IMPLEMENTATION_GUIDE.md     # Detailed implementation docs
├── .gitignore                  # Git ignore rules
├── test_api.sh                 # Testing script
│
├── ui-backend/                 # User Interface Backend Service
│   ├── Dockerfile              # Container configuration
│   ├── requirements.txt        # Python dependencies
│   ├── app.py                  # Flask application
│   ├── uploads/                # Uploaded images (temporary)
│   └── outputs/                # Processed results
│
├── ai-backend/                 # AI Processing Backend Service
│   ├── Dockerfile              # Container configuration
│   ├── requirements.txt        # Python dependencies
│   ├── app.py                  # Flask application
│   ├── utils.py                # YOLO detection utilities
│   ├── models/                 # YOLOv3 model files (auto-downloaded)
│   ├── uploads/                # Received images
│   └── outputs/                # Processed images with boxes
│
└── test_images/                # Sample test images
\\\

## 🛠️ Technology Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Backend Framework** | Flask | 3.0.0 | Lightweight REST API |
| **Computer Vision** | OpenCV | 4.8.1 | Image processing & DNN |
| **Object Detection** | YOLOv3 | - | Real-time detection |
| **Containerization** | Docker | Latest | Environment consistency |
| **Orchestration** | Docker Compose | Latest | Multi-container mgmt |
| **Language** | Python | 3.9 | Primary language |

## 📊 Performance

- **Model loading**: 5-10 seconds (one-time at startup)
- **Detection per image**: 2-5 seconds (CPU)
- **Memory usage**: ~1.5GB (AI backend)
- **Supported formats**: JPG, JPEG, PNG
- **Max file size**: 16MB
- **Detectable objects**: 80 classes (COCO dataset)

## 🔧 Configuration

### Environment Variables

Edit \docker-compose.yml\ to customize:

\\\yaml
environment:
  - AI_BACKEND_URL=http://ai-backend:5001  # AI service URL
\\\

### Detection Parameters

Edit \i-backend/utils.py\:

\\\python
def detect_objects(image, net, classes, output_layers, 
                   conf_threshold=0.5,    # Confidence threshold
                   nms_threshold=0.4):    # NMS threshold
\\\

## 🐛 Troubleshooting

### Port Already in Use
\\\yaml
# Change port in docker-compose.yml
ports:
  - "5050:5000"  # Use 5050 instead of 5000
\\\

### Out of Memory
Increase Docker memory limit to 4GB+ in Docker Desktop settings.

### Model Download Fails
\\\ash
# Rebuild without cache
docker-compose build --no-cache ai-backend
\\\

### Services Can't Communicate
\\\ash
# Check network
docker network ls
docker network inspect object-detection-microservice_app-network

# Test connectivity
docker exec object-detection-microservice-ui-backend-1 ping ai-backend
\\\

## 🛑 Stopping Services

\\\ash
# Stop containers
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Remove everything including images
docker-compose down -v --rmi all
\\\

## 📚 Documentation

For detailed implementation guide, design decisions, and architecture details:
- [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md) - Complete implementation documentation

## 🧪 Testing

\\\ash
# Run test script (Linux/Mac/Git Bash)
./test_api.sh

# Manual testing
# 1. Health check
curl http://localhost:5000/health

# 2. Upload and detect
curl -X POST -F "image=@test.jpg" http://localhost:5000/detect | jq

# 3. Download result
curl http://localhost:5000/output/test.jpg --output result.jpg
\\\

## 🎯 Use Cases

- **Security & Surveillance**: Detect people, vehicles in camera feeds
- **Retail Analytics**: Count customers, track products
- **Traffic Management**: Vehicle detection and counting
- **Wildlife Monitoring**: Animal detection in camera traps
- **Quality Control**: Object inspection in manufacturing

## 🚀 Future Enhancements

### Planned Features
- [ ] Batch image processing
- [ ] WebSocket for real-time streaming
- [ ] Custom model training support
- [ ] GPU acceleration option
- [ ] Video processing support
- [ ] Kubernetes deployment manifests
- [ ] Prometheus metrics & monitoring
- [ ] Authentication & rate limiting

## 📄 License

This project is created for technical assessment purposes.

## 👤 Author

**Technical Assessment Submission**
- GitHub: [@ullasgh](https://github.com/ullasgh)
- Repository: [object-detection-microservice](https://github.com/ullasgh/object-detection-microservice)

## 🙏 Acknowledgments

- YOLOv3: Joseph Redmon - https://pjreddie.com/darknet/yolo/
- COCO Dataset: https://cocodataset.org/
- OpenCV: https://opencv.org/
- Flask: https://flask.palletsprojects.com/

---

**Built with ❤️ for production-ready AI microservices**
