from ultralytics import YOLO #type:ignore

#Load Model
model = YOLO("yolov8n.pt") # builds new model from a pretrained model 

# use model
results = model.train(data="data.yaml", epochs=20) # train the model



