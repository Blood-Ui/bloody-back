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
