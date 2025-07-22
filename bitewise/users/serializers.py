from rest_framework import serializers
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