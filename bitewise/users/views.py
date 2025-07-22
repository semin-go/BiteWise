from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.schemas import openapi
from drf_yasg.utils import swagger_auto_schema
from .serializers import UserSignupSerializer
from .serializers import UserLoginSerializer

class UserSignupView(APIView) :
    @swagger_auto_schema(request_body=UserSignupSerializer)
    def post(self, request) :
        serializer = UserSignupSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message' : '회원가입 성공!' }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView) :
    @swagger_auto_schema(request_body=UserLoginSerializer)
    def post(self, request) :
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            return Response({
                'message' : '로그인 성공!',
                'email' : user.email,
                'name' : user.name,
            },status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)