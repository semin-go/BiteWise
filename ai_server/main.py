from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
import shutil
import uuid
import os

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = YOLO("runs/classify/food_cls/weights/best.pt")  # 경로는 실제 모델 위치에 따라 수정

@app.get("/")
def read_root():
    return {"message": "swagger 체크"}

@app.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    file_ext = file.filename.split(".")[-1]
    temp_filename = f"temp_{uuid.uuid4()}.{file_ext}"
    file_path = os.path.join("ai_server", temp_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2. 이미지 분류 실행
    results = model(file_path)
    predicted_label = results[0].probs.argmax().item()  # 가장 높은 확률의 인덱스
    class_name = model.names[predicted_label] if model.names else f"class_{predicted_label}"


    os.remove(file_path)

    return {"predicted_label": class_name}
