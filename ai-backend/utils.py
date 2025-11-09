import cv2
import numpy as np
import os

def load_yolo_model(model_folder):
    weights_path = os.path.join(model_folder, 'yolov3.weights')
    config_path = os.path.join(model_folder, 'yolov3.cfg')
    names_path = os.path.join(model_folder, 'coco.names')
    
    with open(names_path, 'r') as f:
        classes = [line.strip() for line in f.readlines()]
    
    net = cv2.dnn.readNet(weights_path, config_path)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
    
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    
    return net, classes, output_layers

def detect_objects(image, net, classes, output_layers, conf_threshold=0.5, nms_threshold=0.4):
    height, width = image.shape[:2]
    
    blob = cv2.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    
    outputs = net.forward(output_layers)
    
    boxes = []
    confidences = []
    class_ids = []
    
    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            
            if confidence > conf_threshold:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    
    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
    
    detections = []
    if len(indices) > 0:
        for i in indices.flatten():
            x, y, w, h = boxes[i]
            detections.append({
                'class': classes[class_ids[i]],
                'confidence': round(confidences[i], 4),
                'bounding_box': {
                    'x': x,
                    'y': y,
                    'width': w,
                    'height': h
                }
            })
    
    return detections

def draw_detections(image, detections):
    for det in detections:
        bbox = det['bounding_box']
        x, y, w, h = bbox['x'], bbox['y'], bbox['width'], bbox['height']
        
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        label = f"{det['class']}: {det['confidence']:.2f}"
        cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.5, (0, 255, 0), 2)
    
    return image
