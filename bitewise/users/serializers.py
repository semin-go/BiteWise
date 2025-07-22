from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User

class UserSignupSerializer(serializers.ModelSerializer) :
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'email', 'name', 'password',
            'gender', 'age', 'height',
            'current_weight', 'target_weight', 'diet_plan'
        )

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
class UserLoginSerializer(serializers.Serializer) :
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("이메일 또는 비밀번호가 올바르지 않습니다.")
        data['user'] = user
        return data