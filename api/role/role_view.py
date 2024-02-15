import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.models import Role, UserRoleLink
from api.utils import CustomResponse, get_user_id
from .role_serializer import RoleDropDownSerializer, RoleListSerializer, RoleCreateEditSerializer, UserRoleListSerializer, UserRoleCreateSerializer, UserRoleUpdateSerializer


class RoleDropDownAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        roles = Role.objects.all()
        serializer = RoleDropDownSerializer(roles, many=True)
        return CustomResponse(message="successfully obtained roles", data=serializer.data).success_response()

class RoleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        roles = Role.objects.all()
        serializer = RoleListSerializer(roles, many=True)
        return CustomResponse(message="successfully obtained roles", data=serializer.data).success_response()
    
    def post(self, request):
        user_id = get_user_id(request)
        serializer = RoleCreateEditSerializer(data=request.data, context={'request': request, 'user_id': user_id})

        if serializer.is_valid():
            serializer.save()
            return CustomResponse(message="successfully created role", data=serializer.data).success_response()
        return CustomResponse(message="failed to create role", data=serializer.errors).failure_reponse()
    
    def patch(self, request, role_id):
        user_id = get_user_id(request)
        role = Role.objects.filter(id=role_id).first()
        if not role:
            return CustomResponse(message="role does not exist").failure_reponse()
        serializer = RoleCreateEditSerializer(role, data=request.data, context={'request': request, 'user_id': user_id})
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(message="successfully updated role", data=serializer.data).success_response()
        return CustomResponse(message="failed to update role", data=serializer.errors).failure_reponse()
    
    def delete(self, request, role_id):
        role = Role.objects.filter(id=role_id).first()
        if not role:
            return CustomResponse(message="role does not exist").failure_reponse()
        role.delete()
        return CustomResponse(message="successfully deleted role").success_response()
    
class UserRoleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_roles = UserRoleLink.objects.all()
        serializer = UserRoleListSerializer(user_roles, many=True)
        return CustomResponse(message="successfully obtained roles", data=serializer.data).success_response()
    
    def post(self, request):
        user_id = get_user_id(request)
        serializer = UserRoleCreateSerializer(data=request.data, context={'request': request, 'user_id': user_id})

        if serializer.is_valid():
            serializer.save()
            return CustomResponse(message="successfully created role", data=serializer.data).success_response()
        return CustomResponse(message="failed to create role", data=serializer.errors).failure_reponse()
    
    def patch(self, request, user_role_id):
        user_id = get_user_id(request)
        user_role = UserRoleLink.objects.filter(id=user_role_id).first()
        if not user_role:
            return CustomResponse(message="user role does not exist").failure_reponse()
        serializer = UserRoleUpdateSerializer(user_role, data=request.data, context={'request': request, 'user_id': user_id})
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(message="successfully updated role", data=serializer.data).success_response()
        return CustomResponse(message="failed to update role", data=serializer.errors).failure_reponse()
    
    def delete(self, request, user_role_id):
        user_role = UserRoleLink.objects.filter(id=user_role_id).first()
        if not user_role:
            return CustomResponse(message="user role does not exist").failure_reponse()
        user_role.delete()
        return CustomResponse(message="successfully deleted role").success_response()