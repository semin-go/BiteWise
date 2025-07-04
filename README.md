# BiteWise: AI 기반 식단 분석 및 추천 앱

## 📌 개요
BiteWise는 음식 사진을 분석하여 칼로리, 영양소를 자동 추출하고 맞춤형 식단을 추천하는 헬스케어 애플리케이션입니다.

## 🎯 주요 기능
- YOLOv8로 음식 이미지 인식 및 분류
- EasyOCR로 성분표 인식 및 영양소 정보 추출
- 사용자 맞춤형 식단 추천 및 섭취 기록
- Flutter 앱 UI 및 대시보드 시각화

## ⚙️ 기술 스택
- **Frontend**: Flutter
- **Backend**: Django REST API
- **AI Server**: FastAPI + YOLOv8, EasyOCR
- **DB**: MariaDB
- **Data**: AIHub, Kaggle Food-11

## 🚀 실행 방법

### 1. Python 환경 구축
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
