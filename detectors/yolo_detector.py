from ultralytics import YOLO
import numpy as np

class YOLODetector:
    def __init__(self, model_path='yolov8n.pt', confidence_threshold=0.3):
        self.model = YOLO(model_path)
        self.conf_thresh = confidence_threshold
        self.target_classes = ['person', 'door']

    def detect(self, frame):
        results = self.model(frame, verbose=False)[0]
        detections = []
        door_detection = None
        max_door_conf = -1

        for box in results.boxes:
            class_id = int(box.cls[0])
            conf = float(box.conf[0])
            class_name = self.model.names[class_id]

            if conf >= self.conf_thresh:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                if class_name == 'person':
                    detections.append(([x1, y1, x2 - x1, y2 - y1], conf, 'person'))
                elif class_name == 'door':
                    if conf > max_door_conf:
                        max_door_conf = conf
                        door_detection = [x1, y1, x2, y2]

        return detections, door_detection
