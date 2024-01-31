import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.models import Blood_Group
from .blood_group_serializer import BloodGroupDropDownSerizlizer

class Blood_Group_DropdownAPIview(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        blood_groups = Blood_Group.objects.all()
        serializer = BloodGroupDropDownSerizlizer(blood_groups, many=True)
        return Response({"message": "successfully obtained roles", "response": serializer.data}, status=status.HTTP_200_OK)