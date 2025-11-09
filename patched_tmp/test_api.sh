#!/bin/bash

echo "Testing Object Detection API"
echo "=============================="

echo -e "\n1. Checking UI Backend health..."
curl -s http://localhost:5000/health | jq

echo -e "\n2. Checking AI Backend health..."
curl -s http://localhost:5001/health | jq

echo -e "\n3. Testing object detection..."
if [ -f "test_images/sample.jpg" ]; then
    echo "Uploading test_images/sample.jpg..."
    curl -s -X POST -F "image=@test_images/sample.jpg" \
      http://localhost:5000/detect | jq
else
    echo "⚠ No test image found at test_images/sample.jpg"
    echo "Please add a test image and run again."
fi

echo -e "\n=============================="
echo "Test complete!"
