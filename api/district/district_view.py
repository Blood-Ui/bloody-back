import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.models import District
from .district_serializer import DistrictCreateEditSerializer, DistrictListSerializer, DistrictDropDownSerializer

class DistrictAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        districts = District.objects.all()
        serializer = DistrictListSerializer(districts, many=True)
        return Response({"message": "successfully fetched districts", "response": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)
        if response is not None:
            # unpacking
            user , token = response
            user_id = token.payload['user_id']
        serializer = DistrictCreateEditSerializer(data=request.data, context={'request': request, 'user_id': user_id})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "successfully created district", "response": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"message": "failed to create district", "response": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, district_id):
        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)
        if response is not None:
            # unpacking
            user , token = response
            user_id = token.payload['user_id']
        district = District.objects.get(id=district_id)
        if not district:
            return Response({"message": "district not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = DistrictCreateEditSerializer(district, data=request.data, context={'request': request, 'user_id': user_id})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "successfully updated district", "response": serializer.data}, status=status.HTTP_200_OK)
        return Response({"message": "failed to update district", "response": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, district_id):
        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)
        if response is not None:
            # unpacking
            user , token = response
            user_id = token.payload['user_id']
        district = District.objects.get(id=district_id)
        if not district:
            return Response({"message": "district not found"}, status=status.HTTP_404_NOT_FOUND)
        district.delete()
        return Response({"message": "successfully deleted district"}, status=status.HTTP_204_NO_CONTENT)
    
class DistrictDropDownAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        districts = District.objects.all()
        serializer = DistrictDropDownSerializer(districts, many=True)
        return Response({"message": "successfully fetched districts", "response": serializer.data}, status=status.HTTP_200_OK)