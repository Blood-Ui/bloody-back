from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from tempfile import NamedTemporaryFile
from io import BytesIO
from django.http import FileResponse
from openpyxl import Workbook
from openpyxl.styles import Font

from api.models import Blood_Group
from api.utils import CustomResponse, get_user_id, RoleList, allowed_roles, get_excel_data
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
            excel_file = request.FILES["blood_groups"]
        except:
            return CustomResponse(message="file not found").failure_reponse()
        if not excel_file.name.endswith('.xlsx'):
            return CustomResponse(message="file type not supported").failure_reponse()
        excel_data = get_excel_data(excel_file)
        
        headers = ['name']
        if not excel_data:
            return CustomResponse(message="The file is empty.").failure_reponse()
        for header in headers:
            if header not in excel_data[0]:
                return CustomResponse(message=f"Please provide the {header} in the file.").failure_reponse()
            
        user_id = get_user_id(request)
        serializer = BloodGroupCreateEditSerializer(data=excel_data[1:], context={'request': request, 'user_id': user_id}, many=True)
        with transaction.atomic():
            if serializer.is_valid():
                if len(serializer.data) != len(excel_data[1:]):
                    transaction.set_rollback(True)
                    return CustomResponse(message="something went wrong, please try again", data=serializer.errors).failure_reponse()
                serializer.save()
                return CustomResponse(message="successfully imported blood groups", data=serializer.data).success_response()
        errors_with_indices = []
        for index, error in enumerate(serializer.errors):
            errors_with_indices.append({"row_index": index + 2, "error": error if error else "no error"})  # Adjust index for headers
        return CustomResponse(message="failed to import blood groups", data=errors_with_indices).failure_reponse()

class Blood_Group_Base_Template_APIview(APIView):
    permission_classes = [IsAuthenticated]

    @allowed_roles([RoleList.ADMIN.value])
    def get(self, request):
        wb = Workbook()
        ws = wb.active
        ws.title = "Sheet1"
        ws.append(["name"])
        # Set column headers font as bold
        bold_font = Font(bold=True)
        for cell in ws[1]:
            cell.font = bold_font
        # Set column width
        ws.column_dimensions['A'].width = 30
        wb.save('blood_group_base_template.xlsx')
        with NamedTemporaryFile() as tmp:
            tmp.close()  # with statement opened tmp, close it so wb.save can open it
            wb.save(tmp.name)
            with open(tmp.name, 'rb') as f:
                f.seek(0)
                new_file_object = f.read()
        return FileResponse(BytesIO(new_file_object), as_attachment=True, filename='blood_group_base_template.xlsx')