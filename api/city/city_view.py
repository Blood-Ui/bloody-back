from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.models import City
from .city_serializer import CityCreateSerializer, CityListSerializer

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
            return Response({"message": "successfully created city", "response": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"message": "failed to create city", "response": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        cities = City.objects.all()
        serializer = CityListSerializer(cities, many=True)
        return Response({"message": "successfully fetched cities", "response": serializer.data}, status=status.HTTP_200_OK)