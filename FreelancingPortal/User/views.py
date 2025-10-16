from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView as SimpleJwtTokenObtainPairView
import jwt
from .models import User
import datetime

from .serializers import (
    RegisterSerializer,
    MyTokenObtainPairSerializer, 
    LogoutSerializer,
)

class RegisterAPIView(APIView):
    print("Request Recived")
    permission_classes = [AllowAny]
    print("Allowed Operation to user")
    serializer_class = RegisterSerializer
    print("Serializer initialized")

    def post(self, request):
        print("In side post function")
        serializer = self.serializer_class(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        print("Data validated by serializer")
        user = serializer.save()
        print("Data Stored by serializer in DB")
        
        refresh = RefreshToken.for_user(user)
        print("Refresh Token generated")

        return Response({
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

class LoginTokenObtainPairAPIView(SimpleJwtTokenObtainPairView, APIView):
    permission_classes = [AllowAny]
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request):
        
        user = User.objects.filter(email=request.data.get('email')).first()

        if user:
            user.last_login = datetime.datetime.now()
            user.save()
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                return Response(serializer.validated_data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            refresh_token = serializer.validated_data["refresh_token"]
            token = RefreshToken(refresh_token)
            print("access Token")
            print(token.access_token)   # access token
            print("refresh Token")
            print(token)  # Refresh token 

            token.blacklist()
            
            return Response(
                {"detail": "Successfully logged out."},
                status=status.HTTP_205_RESET_CONTENT
            )
        except Exception:
            return Response(
                {"detail": "Invalid or expired token provided."},
                status=status.HTTP_400_BAD_REQUEST
            )
        


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if not user.check_password(old_password):
            return Response({"error": "Old password is incorrect"}, status=400)
        
        if old_password == new_password:
            return Response(({"error":"New Password can not be same as previous one !"}))
        
        if new_password != confirm_password:
            return Response({
                "error": "New password and confirm password do not match"}, status=400)

        user.set_password(new_password)
        user.save()

        return Response({"message": "Password changed successfully"})