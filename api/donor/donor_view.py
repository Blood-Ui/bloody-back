from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from api.models import Donor
from api.utils import CustomResponse, get_user_id
from .donor_serializer import DonorCreateSerializer, DonorUpdateSerializer, DonorListSerializer, DonorDropDownSerializer


class DonorAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user_id = get_user_id(request)
        serializer = DonorCreateSerializer(data=request.data, context={"request": request, "user_id": user_id})
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(message="successfully created donor", data=serializer.data).success_response()
        return CustomResponse(message="failed to create donor", data=serializer.errors).failure_reponse()
    
    def get(self, request):
        donors = Donor.objects.all()
        serializer = DonorListSerializer(donors, many=True)
        return CustomResponse(message="successfully obtained donors", data=serializer.data).success_response()
    
    def patch(self, request, donor_id):
        user_id = get_user_id(request)
        if not Donor.objects.filter(id=donor_id).exists():
            return CustomResponse(message="donor not found").failure_reponse()
        donor = Donor.objects.get(id=donor_id)
        serializer = DonorUpdateSerializer(donor, data=request.data, context={"request": request, "user_id": user_id})
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(message="successfully updated donor", data=serializer.data).success_response()
        return CustomResponse(message="failed to update donor", data=serializer.errors).failure_reponse()
    
    def delete(self, request, donor_id):
        if not Donor.objects.filter(id=donor_id).exists():
            return CustomResponse(message="donor not found").failure_reponse()
        donor = Donor.objects.get(id=donor_id)
        donor.delete()
        return CustomResponse(message="successfully deleted donor").success_response()
    
class DonorDropDownAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        donors = Donor.objects.all()
        serializer = DonorDropDownSerializer(donors, many=True)
        return CustomResponse(message="successfully obtained donors", data=serializer.data).success_response()