from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.schemas import openapi
from drf_yasg.utils import swagger_auto_schema
from .serializers import UserSignupSerializer

class UserSignupView(APIView) :
    @swagger_auto_schema(request_body=UserSignupSerializer)
    def post(self, request) :
        serializer = UserSignupSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message' : '회원가입 성공!' }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)