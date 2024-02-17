from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from api.models import City, District
from api.utils import CustomResponse, get_user_id, RoleList, allowed_roles
from .city_serializer import CityCreateSerializer, CityListSerializer, CityUpdateSerializer, CityDropDownSerializer

class CityAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @allowed_roles([RoleList.ADMIN.value])
    def post(self, request):
        user_id = get_user_id(request)
        serializer = CityCreateSerializer(data=request.data, context={'request': request, 'user_id': user_id})
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(message="successfully created city", data=serializer.data).success_response()
        return CustomResponse(message="failed to create city", data=serializer.errors).failure_reponse()
    
    @allowed_roles([RoleList.ADMIN.value])
    def get(self, request):
        cities = City.objects.all()
        serializer = CityListSerializer(cities, many=True)
        return CustomResponse(message="successfully obtained cities", data=serializer.data).success_response()
    
    @allowed_roles([RoleList.ADMIN.value])
    def patch(self, request, city_id):
        user_id = get_user_id(request)
        if not City.objects.filter(id=city_id).exists():
            return CustomResponse(message="city does not exist").failure_reponse()
        city = City.objects.get(id=city_id)
        serializer = CityUpdateSerializer(city, data=request.data, context={'request': request, 'user_id': user_id})
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(message="successfully updated city", data=serializer.data).success_response()
        return CustomResponse(message="failed to update city", data=serializer.errors).failure_reponse()
    
    @allowed_roles([RoleList.ADMIN.value])
    def delete(self, request, city_id):
        if not City.objects.filter(id=city_id).exists():
            return CustomResponse(message="city does not exist").failure_reponse()
        city = City.objects.get(id=city_id)
        city.delete()
        return CustomResponse(message="successfully deleted city").success_response()
    
class CityDropDownView(APIView):
    permission_classes = [IsAuthenticated]

    @allowed_roles([RoleList.ADMIN.value])
    def get(self, request, district_id):
        if not District.objects.filter(id=district_id).exists():
            return CustomResponse(message="district does not exist").failure_reponse()
        if not City.objects.filter(district=district_id).exists():
            return CustomResponse(message="No city is present for this district").failure_reponse()
        cities = City.objects.filter(district=district_id)
        serializer = CityDropDownSerializer(cities, many=True)
        return CustomResponse(message="successfully obtained cities", data=serializer.data).success_response()