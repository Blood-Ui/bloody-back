import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.models import District
from api.utils import CustomResponse, get_user_id
from .district_serializer import DistrictCreateEditSerializer, DistrictListSerializer, DistrictDropDownSerializer

class DistrictAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        districts = District.objects.all()
        serializer = DistrictListSerializer(districts, many=True)
        return CustomResponse(message="successfully obtained districts", data=serializer.data).success_response()

    def post(self, request):
        user_id = get_user_id(request)
        serializer = DistrictCreateEditSerializer(data=request.data, context={'request': request, 'user_id': user_id})
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(message="successfully created district", data=serializer.data).success_response()
        return CustomResponse(message="failed to create district", data=serializer.errors).failure_reponse()
    
    def patch(self, request, district_id):
        user_id = get_user_id(request)
        if not District.objects.filter(id=district_id).exists():
            return CustomResponse(message="district not found").failure_reponse()
        district = District.objects.get(id=district_id)
        serializer = DistrictCreateEditSerializer(district, data=request.data, context={'request': request, 'user_id': user_id})
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(message="successfully updated district", data=serializer.data).success_response()
        return CustomResponse(message="failed to update district", data=serializer.errors).failure_reponse()
    
    def delete(self, request, district_id):
        if not District.objects.filter(id=district_id).exists():
            return CustomResponse(message="district not found").failure_reponse()
        district = District.objects.get(id=district_id)
        district.delete()
        return CustomResponse(message="successfully deleted district").success_response()
    
class DistrictDropDownAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        districts = District.objects.all()
        serializer = DistrictDropDownSerializer(districts, many=True)
        return CustomResponse(message="successfully obtained districts", data=serializer.data).success_response()