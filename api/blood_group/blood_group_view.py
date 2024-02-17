from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from api.models import Blood_Group
from api.utils import CustomResponse, get_user_id
from .blood_group_serializer import BloodGroupDropDownSerizlizer, BloodGroupListSerializer, BloodGroupCreateEditSerializer

class Blood_Group_DropdownAPIview(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        blood_groups = Blood_Group.objects.all()
        serializer = BloodGroupDropDownSerizlizer(blood_groups, many=True)
        return CustomResponse(message="successfully obtained blood groups", data=serializer.data).success_response()
    
class Blood_Group_APIview(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        blood_groups = Blood_Group.objects.all()
        serializer = BloodGroupListSerializer(blood_groups, many=True)
        return CustomResponse(message="successfully obtained blood groups", data=serializer.data).success_response()
    
    def post(self, request):
        user_id = get_user_id(request)
        serializer = BloodGroupCreateEditSerializer(data=request.data, context={'request': request, 'user_id': user_id})
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(message="successfully created blood group", data=serializer.data).success_response()
        return CustomResponse(message="failed to blood group", data=serializer.errors).failure_reponse()
    
    def patch(self, request, blood_group_id):
        user_id = get_user_id(request)
        if not Blood_Group.objects.filter(id=blood_group_id).exists():
            return CustomResponse(message="blood group not found").failure_reponse()
        blood_group = Blood_Group.objects.get(id=blood_group_id)
        serializer = BloodGroupCreateEditSerializer(blood_group, data=request.data, context={'request': request, 'user_id': user_id})
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(message="successfully updated blood group", data=serializer.data).success_response()
        return CustomResponse(message="failed to update blood group", data=serializer.errors).failure_reponse()
    
    def delete(self, request, blood_group_id):
        if not Blood_Group.objects.filter(id=blood_group_id).exists():
            return CustomResponse(message="blood group not found").failure_reponse()
        blood_group = Blood_Group.objects.get(id=blood_group_id)
        blood_group.delete()
        return CustomResponse(message="successfully deleted blood group").success_response()