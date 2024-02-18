from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import openpyxl

from api.models import Blood_Group
from api.utils import CustomResponse, get_user_id, RoleList, allowed_roles
from .blood_group_serializer import BloodGroupDropDownSerizlizer, BloodGroupListSerializer, BloodGroupCreateEditSerializer

class Blood_Group_DropdownAPIview(APIView):
    permission_classes = [IsAuthenticated]

    @allowed_roles([RoleList.ADMIN.value])
    def get(self, request):
        blood_groups = Blood_Group.objects.all()
        serializer = BloodGroupDropDownSerizlizer(blood_groups, many=True)
        return CustomResponse(message="successfully obtained blood groups", data=serializer.data).success_response()
    
class Blood_Group_APIview(APIView):
    permission_classes = [IsAuthenticated]

    @allowed_roles([RoleList.ADMIN.value])
    def get(self, request):
        blood_groups = Blood_Group.objects.all()
        serializer = BloodGroupListSerializer(blood_groups, many=True)
        return CustomResponse(message="successfully obtained blood groups", data=serializer.data).success_response()
    
    @allowed_roles([RoleList.ADMIN.value])
    def post(self, request):
        user_id = get_user_id(request)
        serializer = BloodGroupCreateEditSerializer(data=request.data, context={'request': request, 'user_id': user_id})
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(message="successfully created blood group", data=serializer.data).success_response()
        return CustomResponse(message="failed to blood group", data=serializer.errors).failure_reponse()
    
    @allowed_roles([RoleList.ADMIN.value])
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
    
    @allowed_roles([RoleList.ADMIN.value])
    def delete(self, request, blood_group_id):
        if not Blood_Group.objects.filter(id=blood_group_id).exists():
            return CustomResponse(message="blood group not found").failure_reponse()
        blood_group = Blood_Group.objects.get(id=blood_group_id)
        blood_group.delete()
        return CustomResponse(message="successfully deleted blood group").success_response()
    
class Blood_Group_Bulk_Import_APIview(APIView):
    permission_classes = [IsAuthenticated]

    @allowed_roles([RoleList.ADMIN.value])
    def post(self, request):
        try:
            excel_file = request.FILES['blood_groups']
            if not excel_file.name.endswith('.xlsx'):
                return CustomResponse(message="file type not supported").failure_reponse()
        except:
            return CustomResponse(message="file not found").failure_reponse()
        
        wb = openpyxl.load_workbook(excel_file)
        worksheet = wb.active
        excel_data = list()
        for row in worksheet.iter_rows():
            row_data = list()
            for cell in row:
                row_data.append(cell.value)
            excel_data.append(row_data)
        if not excel_data:
            return CustomResponse(message="no data found in file").failure_reponse()
        
        excel_headers = ['name']
        if excel_data[0] != excel_headers:
            return CustomResponse(message="invalid file format").failure_reponse()
        excel_data = [dict(zip(excel_headers, data)) for data in excel_data[1:]]
        
        user_id = get_user_id(request)
        serializer = BloodGroupCreateEditSerializer(data=excel_data[1:], context={'request': request, 'user_id': user_id}, many=True)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(message="successfully imported blood groups", data=serializer.data).success_response()
        return CustomResponse(message="failed to import blood groups", data=serializer.errors).failure_reponse()