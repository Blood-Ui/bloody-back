from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserRegisterSerializer
from .utils import send_code_to_user
from .models import User, OneTimePassword

class RegisterUserView(GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.data
            send_code_to_user(user['email'])
            return Response({
                "data": user,
                "message": f'hi {user["first_name"]}, thanks for signing up, a passcode has been sent to your email address {user["email"]}'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VerifyUserEmail(GenericAPIView):
    def post(self, request):
        otpcode = request.data.get('otp')
        try:
            user_code_obj = OneTimePassword.objects.get(code=otpcode)
            user = user_code_obj.user
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return Response({
                    "message": 'account email verified successfully'
                }, status = status.HTTP_200_OK)
            return Response({
                "message": 'account email already verified'
            }, status = status.HTTP_204_NO_CONTENT)
        except OneTimePassword.DoesNotExist:
            return Response({
                "message": 'passcode not provided or is invalid'
            }, status = status.HTTP_400_BAD_REQUEST) 