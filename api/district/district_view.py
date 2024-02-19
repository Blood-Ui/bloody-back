import uuid
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from api.models import District
from api.utils import CustomResponse, get_user_id, RoleList, allowed_roles, get_excel_data, generate_excel_template
from .district_serializer import DistrictCreateEditSerializer, DistrictListSerializer, DistrictDropDownSerializer

class DistrictAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @allowed_roles([RoleList.ADMIN.value])
    def get(self, request):
        districts = District.objects.all()
        serializer = DistrictListSerializer(districts, many=True)
        return CustomResponse(message="successfully obtained districts", data=serializer.data).success_response()

    @allowed_roles([RoleList.ADMIN.value])
    def post(self, request):
        user_id = get_user_id(request)
        serializer = DistrictCreateEditSerializer(data=request.data, context={'request': request, 'user_id': user_id})
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(message="successfully created district", data=serializer.data).success_response()
        return CustomResponse(message="failed to create district", data=serializer.errors).failure_reponse()
    
    @allowed_roles([RoleList.ADMIN.value])
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
    
    @allowed_roles([RoleList.ADMIN.value])
    def delete(self, request, district_id):
        if not District.objects.filter(id=district_id).exists():
            return CustomResponse(message="district not found").failure_reponse()
        district = District.objects.get(id=district_id)
        district.delete()
        return CustomResponse(message="successfully deleted district").success_response()
    
class DistrictDropDownAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @allowed_roles([RoleList.ADMIN.value])
    def get(self, request):
        districts = District.objects.all()
        serializer = DistrictDropDownSerializer(districts, many=True)
        return CustomResponse(message="successfully obtained districts", data=serializer.data).success_response()
    
class DistrictBaseTemplateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @allowed_roles([RoleList.ADMIN.value])
    def get(self, request):
        sheet_names = ['Sheet1']
        headers = [['name']]
        column_widths = {'A': 35}
        filename = "district_base_template.xlsx"
        
        response = generate_excel_template(sheet_names, filename, headers, column_widths)
        return response

class DistrictBulkImportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @allowed_roles([RoleList.ADMIN.value])
    def post(self, request):
        try:
            excel_file = request.FILES["districts"]
        except:
            return CustomResponse(message="districts file not found").failure_reponse()
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
        serializer = DistrictCreateEditSerializer(data=excel_data[1:], many=True, context={'request': request, 'user_id': user_id})
        with transaction.atomic():
            if serializer.is_valid():
                if len(serializer.data) != len(excel_data[1:]):
                    transaction.set_rollback(True)
                    return CustomResponse(message="something went wrong, please try again", data=serializer.errors).failure_reponse()
                serializer.save()
                return CustomResponse(message="successfully imported districts", data=serializer.data).success_response()
        errors_with_indices = []
        for index, error in enumerate(serializer.errors):
            errors_with_indices.append({"row_index": index + 2, "error": error if error else "no error"})  # Adjust index for headers
        return CustomResponse(message="failed to import districts", data=errors_with_indices).failure_reponse()