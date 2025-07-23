from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from paddleocr import PaddleOCR
from PIL import Image
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import OCRUploadSerializer

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

        # 이미지 로드
        image = Image.open(image_file)
        result = ocr_model.ocr(image)
        texts = [line[1][0] for box in result for line in box]

        # 영양성분 추출
        nutrition_data = self.extract_nutrition_data(texts)
        if not nutrition_data:
            return Response({'error': '영양성분을 찾을 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # DB 저장
        nutrition_serializer = NutritionSerializer(data=nutrition_data)
        if nutrition_serializer.is_valid():
            nutrition_serializer.save()
            return Response(nutrition_serializer.data, status=status.HTTP_201_CREATED)

        return Response(nutrition_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def extract_nutrition_data(self, texts):
        data = {}

        for text in texts:
            # 칼로리
            if '칼로리' in text or '열량' in text:
                match = re.search(r'(\d+)\s*k?cal', text.lower())
                if match:
                    data['calories'] = int(match.group(1))

            # 탄수화물
            elif '탄수화물' in text:
                match = re.search(r'(\d+\.?\d*)\s*g', text.lower())
                if match:
                    data['carbohydrate'] = float(match.group(1))

            # 단백질
            elif '단백질' in text:
                match = re.search(r'(\d+\.?\d*)\s*g', text.lower())
                if match:
                    data['protein'] = float(match.group(1))

            # 지방        
            elif '지방' in text:
                match = re.search(r'(\d+\.?\d*)\s*g', text.lower())
                if match:
                    data['fat'] = float(match.group(1))

        # 4개가 모두 존재할 때만 반환
        return data if data else None