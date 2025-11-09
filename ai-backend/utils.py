import cv2
import numpy as np
import os

def load_yolo_model(model_folder):
    weights_path = os.path.join(model_folder, 'yolov3.weights')
    config_path = os.path.join(model_folder, 'yolov3.cfg')
    names_path = os.path.join(model_folder, 'coco.names')

    if not (os.path.exists(weights_path) and os.path.exists(config_path) and os.path.exists(names_path)):
        raise FileNotFoundError("Missing YOLO files in model folder")

    with open(names_path, 'r') as f:
        classes = [line.strip() for line in f.readlines()]

    net = cv2.dnn.readNet(weights_path, config_path)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    layer_names = net.getLayerNames()
    try:
        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]
    except AttributeError:
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    return net, classes, output_layers

def detect_objects(net, output_layers, classes, image, conf_threshold=0.5, nms_threshold=0.4, input_size=(416,416)):
    H, W = image.shape[:2]
    blob = cv2.dnn.blobFromImage(image, 1/255.0, input_size, swapRB=True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    boxes, confidences, class_ids = [], [], []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            if len(scores) == 0: continue
            class_id = int(np.argmax(scores))
            confidence = float(scores[class_id])
            if confidence > conf_threshold:
                center_x, center_y, w, h = int(detection[0]*W), int(detection[1]*H), int(detection[2]*W), int(detection[3]*H)
                x, y = int(center_x - w/2), int(center_y - h/2)
                boxes.append([x,y,w,h])
                confidences.append(confidence)
                class_ids.append(class_id)

    idxs = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
    detections = []
    if len(idxs) > 0:
        for i in idxs.flatten():
            x,y,w,h = boxes[i]
            cls = classes[class_ids[i]] if class_ids[i] < len(classes) else str(class_ids[i])
            detections.append({'class': cls, 'confidence': confidences[i],
                               'bounding_box': {'x':x,'y':y,'width':w,'height':h}})
    return detections

def draw_detections(image, detections):
    for det in detections:
        b = det['bounding_box']
        x,y,w,h = b['x'],b['y'],b['width'],b['height']
        cv2.rectangle(image, (x,y), (x+w,y+h), (0,255,0), 2)
        label = f"{det['class']}:{det['confidence']:.2f}"
        cv2.putText(image, label, (x, max(y-10,10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
    return image
