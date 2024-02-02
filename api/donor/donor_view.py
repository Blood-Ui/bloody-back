from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.models import Donor
from .donor_serializer import DonorCreateUpdateSerializer, DonorListSerializer


class DonorAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)
        if response is not None:
            # unpacking
            user , token = response
            user_id = token.payload['user_id']

        serializer = DonorCreateUpdateSerializer(data=request.data, context={"request": request, "user_id": user_id})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "successfully created donor", "response": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"message": "failed to create donor", "response": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        donors = Donor.objects.all()
        serializer = DonorListSerializer(donors, many=True)
        return Response({"message": "successfully fetched donors", "response": serializer.data}, status=status.HTTP_200_OK)
    
    def patch(self, request, donor_id):
        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)
        if response is not None:
            # unpacking
            user , token = response
            user_id = token.payload['user_id']

        donor = Donor.objects.get(id=donor_id)
        if donor is None:
            return Response({"message": "donor not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = DonorCreateUpdateSerializer(donor, data=request.data, context={"request": request, "user_id": user_id})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "successfully updated donor", "response": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"message": "failed to update donor", "response": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, donor_id):
        donor = Donor.objects.get(id=donor_id)
        if donor is None:
            return Response({"message": "donor not found"}, status=status.HTTP_404_NOT_FOUND)
        donor.delete()
        return Response({"message": "successfully deleted donor"}, status=status.HTTP_204_NO_CONTENT)