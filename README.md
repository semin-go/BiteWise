# BiteWise: AI 기반 식단 분석 및 추천 앱

## 📌 개요
BiteWise는 음식 사진을 분석하여 칼로리, 영양소를 자동 추출하고 맞춤형 식단을 추천하는 헬스케어 애플리케이션입니다.

## 🎯 주요 기능
- YOLOv8로 음식 이미지 인식 및 분류
- EasyOCR로 성분표 인식 및 영양소 정보 추출
- 사용자 맞춤형 식단 추천 및 섭취 기록
- Flutter 앱 UI 및 대시보드 시각화

## 🧱 시스템 아키텍처

![스크린샷 2025-07-04 171709](https://github.com/user-attachments/assets/4d35fcf1-2c71-40d9-9c06-a6bb9b269164)


- **Frontend:**
  - Flutter로 모바일 앱 개발
  - 사용자 사진 입력 및 결과 조회 인터페이스 제공

- **Backend (Django):**
  - 사용자 요청 처리, 사용자 정보 및 식단 분석 결과 저장
  - FastAPI AI 서버와 통신하여 분석 요청 전송
  - MariaDB와 연동하여 데이터 저장

- **AI Server (FastAPI):**
  - 음식 이미지 분석을 위한 딥러닝 모델 실행
  - 분석 결과를 Django 서버로 반환
  - Jupyter Notebook 기반 개발 가능

- **Database:**
  - MariaDB를 통해 사용자 정보, 음식 기록, 추천 결과 등 관리

- **Version Control:**
  - Git으로 소스 코드 버전 관리

---

## 🛠️ 기술 스택

| 분야        | 기술                    |
|-------------|-------------------------|
| 프론트엔드  | Flutter                 |
| 백엔드      | Django                  |
| AI 서버     | FastAPI, PyTorch/TensorFlow |
| DB          | MariaDB                |
| 협업 도구   | Git, GitHub             |
| 개발 환경   | Jupyter Notebook        |

---

