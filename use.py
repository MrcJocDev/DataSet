from ultralytics import YOLO # type:ignore
import numpy as np # type:ignore

model = YOLO('runs/detect/train8/weights/best.pt')
results = model('2.jpg', save=True, conf=0.04)
names = model.names

boxes = results[0].boxes.xyxy
class_ids = results[0].boxes.cls

print(class_ids)
gauge_coords = boxes[0]


