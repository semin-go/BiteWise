from rest_framework import serializers
from .models import Nutrition

class NutritionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nutrition
        fields = '__all__'

class OCRUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()