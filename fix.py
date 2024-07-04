from ultralytics import YOLO #type:ignore
import cv2 #type:ignore
 
IMG_PATH = "runs\detect\predict16\predict.jpg"

model = YOLO("runs/detect/train8/weights/best.pt")
results = model(IMG_PATH, save=True, conf=0.1)

boxes = results[0].boxes.xywh
class_ids = results[0].boxes.cls

print(boxes)
image = cv2.imread(IMG_PATH)

"""GAUGE COORDS EXTRACTION"""
# def gaugeCoords():

#     x1, y1, x2, y2 = boxes[0]
#     xcr = (x1 + x2)/2
#     ycr = (y1 + y2)/2
#     return xcr, ycr

# gCoords = gaugeCoords() # Container type list 


x, y, w, h = boxes[0]
top_left = (x, y)
bottom_right = (x+w, y+h)

cropped_image = image[int(top_left[1]):int(bottom_right[1]), int(top_left[0]):int(bottom_right[0])]
cv2.imshow("CROPPED", cropped_image)
cv2.waitKey(0)