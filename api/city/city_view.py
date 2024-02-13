from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.models import City, District
from api.utils import CustomResponse
from .city_serializer import CityCreateSerializer, CityListSerializer, CityUpdateSerializer, CityDropDownSerializer

class CityAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)
        if response is not None:
            # unpacking
            user , token = response
            user_id = token.payload['user_id']
        
        serializer = CityCreateSerializer(data=request.data, context={'request': request, 'user_id': user_id})
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(message="successfully created city", data=serializer.data).success_response()
        return CustomResponse(message="failed to create city", data=serializer.errors).failure_reponse()
    
    def get(self, request):
        cities = City.objects.all()
        serializer = CityListSerializer(cities, many=True)
        return CustomResponse(message="successfully obtained cities", data=serializer.data).success_response()
    
    def patch(self, request, city_id):
        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)
        if response is not None:
            # unpacking
            user , token = response
            user_id = token.payload['user_id']
        if not City.objects.filter(id=city_id).exists():
            return CustomResponse(message="city does not exist").failure_reponse()
        city = City.objects.get(id=city_id)
        serializer = CityUpdateSerializer(city, data=request.data, context={'request': request, 'user_id': user_id})
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(message="successfully updated city", data=serializer.data).success_response()
        return CustomResponse(message="failed to update city", data=serializer.errors).failure_reponse()
    
    def delete(self, request, city_id):
        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)
        if response is not None:
            # unpacking
            user , token = response
            user_id = token.payload['user_id']
        if not City.objects.filter(id=city_id).exists():
            return CustomResponse(message="city does not exist").failure_reponse()
        city = City.objects.get(id=city_id)
        city.delete()
        return CustomResponse(message="successfully deleted city").success_response()
    
class CityDropDownView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, district_id):
        if not District.objects.filter(id=district_id).exists():
            return CustomResponse(message="district does not exist").failure_reponse()
        if not City.objects.filter(district=district_id).exists():
            return CustomResponse(message="No city is present for this district").failure_reponse()
        cities = City.objects.filter(district=district_id)
        serializer = CityDropDownSerializer(cities, many=True)
        return CustomResponse(message="successfully obtained cities", data=serializer.data).success_response()