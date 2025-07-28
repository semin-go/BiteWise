from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from paddleocr import PaddleOCR
from PIL import Image
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import OCRUploadSerializer

import tempfile
import os
import io
import re

from .models import Nutrition
from .serializers import NutritionSerializer

# OCR 모델 초기화
ocr_model = PaddleOCR(use_angle_cls=True, lang="korean")

class OCRUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_description="영양성분표 이미지 업로드",
        request_body=OCRUploadSerializer
    )
    def post(self, request):
        serializer = OCRUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': '이미지를 업로드해주세요'}, status=status.HTTP_400_BAD_REQUEST)

        image_file = serializer.validated_data['image']

        # 이미지 파일을 임시 저장 후 저장 파일로 OCR 수행
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp:
            for chunk in image_file.chunks():
                temp.write(chunk)
            temp_path = temp.name

        try:
            result = ocr_model.predict(temp_path)
            texts = result[0]['rec_texts']
            scores = result[0]['rec_scores']

            print("OCR 결과: ", texts)

            # 영양성분 추출
            nutrition_data = self.extract_nutrition_data(texts, scores)
            if not nutrition_data:
                return Response({'error': '영양성분을 찾을 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # DB 저장
            nutrition_serializer = NutritionSerializer(data=nutrition_data)
            if nutrition_serializer.is_valid():
                nutrition_serializer.save()
                return Response(nutrition_serializer.data, status=status.HTTP_201_CREATED)
            
            return Response(nutrition_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        finally:
            os.remove(temp_path) # 임시 파일 삭제
    
        
    def extract_nutrition_data(self, texts, scores):
        # 신뢰도 필터링 + 정규화
        clean_texts = [
            re.sub(r'\s+', '', text.lower().replace('㎉', 'kcal').replace('omg', '0mg'))
            for text, score in zip(texts, scores) if score >= 0.6
        ]

        print("[DEBUG] Cleaned Texts:", clean_texts)

        data = {'calories': None, 'carbohydrate': None, 'protein': None, 'fat': None}

        i = 0
        while i < len(clean_texts):
            text = clean_texts[i]

            # 칼로리
            print(f"[DEBUG] checking kcal in: {text}")
            match = re.search(r'(\d+(?:\.\d+)?)(?=kcal|㎉)', text)
            if match and '%' not in text:
                data['calories'] = float(match.group(1))
            else:
                for j in range(i + 1, min(i + 4, len(clean_texts))): 
                    print(f"[DEBUG] fallback checking kcal in: {clean_texts[j]}")
                    match = re.search(r'(\d+(?:\.\d+)?)(?=kcal|㎉)', clean_texts[j])
                    if match and '%' not in clean_texts[j]:
                        data['calories'] = int(float(match.group(1)))
                        break

            # 탄수화물
            if '탄수화물' in text:
                match = re.search(r'(\d+(?:\.\d+)?)g', text)
                if match and '%' not in text:
                    data['carbohydrate'] = float(match.group(1))
                else:
                    for j in range(i+1, min(i+4, len(clean_texts))):
                        match = re.search(r'(\d+(?:\.\d+)?)g', clean_texts[j])
                        if match and '%' not in clean_texts[j]:
                            data['carbohydrate'] = float(match.group(1))
                            break
            
            # 단백질
            if '단백질' in text:
                match = re.search(r'(\d+(?:\.\d+)?)g', text)
                if match and '%' not in text:
                    data['protein'] = float(match.group(1))
                else:
                    for j in range(i+1, min(i+4, len(clean_texts))):
                        match = re.search(r'(\d+(?:\.\d+)?)g', clean_texts[j])
                        if match and '%' not in clean_texts[j]:
                            data['protein'] = float(match.group(1))
                            break

            # 지방 (포화지방, 트랜스 제외)
            if '지방' in text and all(x not in text for x in ['포화', '트랜스']):
                # 먼저 현재 줄에서 시도
                match = re.search(r'(\d+(\.\d+)?)g', text)
                if match and '%' not in text:
                    data['fat'] = float(match.group(1))
                else:
                    # 다음 줄들에서 fallback
                    for j in range(i+1, min(i+4, len(clean_texts))):
                        match = re.search(r'(\d+(\.\d+)?)g', clean_texts[j])
                        if match and '%' not in clean_texts[j]:
                            data['fat'] = float(match.group(1))
                            break

            i += 1

        # 기본값 0.0 처리
        for k in data:
            if data[k] is None:
                data[k] = 0.0

        return data