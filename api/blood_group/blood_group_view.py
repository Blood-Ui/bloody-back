import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.models import Blood_Group
from .blood_group_serializer import BloodGroupDropDownSerizlizer, BloodGroupListSerializer

class Blood_Group_DropdownAPIview(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        blood_groups = Blood_Group.objects.all()
        serializer = BloodGroupDropDownSerizlizer(blood_groups, many=True)
        return Response({"message": "successfully obtained blood groups", "response": serializer.data}, status=status.HTTP_200_OK)
    
class Blood_Group_APIview(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        blood_groups = Blood_Group.objects.all()
        serializer = BloodGroupListSerializer(blood_groups, many=True)
        return Response({"message": "successfully obtained blood groups", "response": serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)
        if response is not None:
            # unpacking
            user , token = response
            user_id = token.payload['user_id']
        serializer = BloodGroupListSerializer(data=request.data, context={'request': request, 'user_id': user_id})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "successfully created blood group", "response": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"message": "failed to blood group", "response": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)