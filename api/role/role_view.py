import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.models import Role
from .role_serializer import RoleDropDownSerializer, RoleListSerializer, RoleCreateEditSerializer


class RoleDropDownAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        roles = Role.objects.all()
        serializer = RoleDropDownSerializer(roles, many=True)
        return Response({"message": "successfully obtained roles", "response": serializer.data}, status=status.HTTP_200_OK)

class RoleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        roles = Role.objects.all()
        serializer = RoleListSerializer(roles, many=True)
        return Response({"message": "successfully obtained roles", "response": serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)
        if response is not None:
            # unpacking
            user , token = response
            user_id = token.payload['user_id']
        serializer = RoleCreateEditSerializer(data=request.data, context={'request': request, 'user_id': user_id})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "successfully created role", "response": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"message": "failed to create role", "response": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, role_id):
        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)
        if response is not None:
            # unpacking
            user , token = response
            user_id = token.payload['user_id']
        role = Role.objects.filter(id=role_id).first()
        if not role:
            return Response({"message": "role does not exist"}, status=status.HTTP_404_NOT_FOUND)
        serializer = RoleCreateEditSerializer(role, data=request.data, context={'request': request, 'user_id': user_id})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "successfully updated role", "response": serializer.data}, status=status.HTTP_200_OK)
        return Response({"message": "failed to update role", "response": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)