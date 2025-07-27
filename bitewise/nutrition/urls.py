from django.urls import path
from .views import OCRUploadView

urlpatterns = [
    path('ocr/', OCRUploadView.as_view(), name='ocr-upload'),
]