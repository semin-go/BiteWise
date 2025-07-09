from ultralytics import YOLO


model = YOLO("yolov8n-cls.pt") #모델 바꿔도 됨 

# model.train(
#     data="dataset/training",          # 학습 데이터 폴더
#     val="dataset/validation",         # 검증 데이터 폴더
#     epochs=50,
#     imgsz=224,
#     batch=32,
#     project="runs",
#     name="food_cls"
# )

model.train(
    data="dataset",  # 'dataset/train', 'dataset/valid' 구조여야 함
    epochs=30,
    imgsz=224,
    project="runs/classify",
    name="food_cls",
    pretrained=True
)