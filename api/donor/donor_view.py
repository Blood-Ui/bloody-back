from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from api.models import Donor, Blood_Group, City
from api.utils import CustomResponse, get_user_id, RoleList, allowed_roles, get_excel_data, generate_excel_template
from .donor_serializer import DonorCreateSerializer, DonorUpdateSerializer, DonorListSerializer, DonorDropDownSerializer


class DonorAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @allowed_roles([RoleList.ADMIN.value])
    def post(self, request):
        user_id = get_user_id(request)
        serializer = DonorCreateSerializer(data=request.data, context={"request": request, "user_id": user_id})
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(message="successfully created donor", data=serializer.data).success_response()
        return CustomResponse(message="failed to create donor", data=serializer.errors).failure_reponse()
    
    @allowed_roles([RoleList.ADMIN.value])
    def get(self, request):
        donors = Donor.objects.all()
        serializer = DonorListSerializer(donors, many=True)
        return CustomResponse(message="successfully obtained donors", data=serializer.data).success_response()
    
    @allowed_roles([RoleList.ADMIN.value])
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
    
    @allowed_roles([RoleList.ADMIN.value])
    def delete(self, request, donor_id):
        if not Donor.objects.filter(id=donor_id).exists():
            return CustomResponse(message="donor not found").failure_reponse()
        donor = Donor.objects.get(id=donor_id)
        donor.delete()
        return CustomResponse(message="successfully deleted donor").success_response()
    
class DonorDropDownAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @allowed_roles([RoleList.ADMIN.value])
    def get(self, request):
        donors = Donor.objects.all()
        serializer = DonorDropDownSerializer(donors, many=True)
        return CustomResponse(message="successfully obtained donors", data=serializer.data).success_response()
    
class DonorBaseTemplateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @allowed_roles([RoleList.ADMIN.value])
    def get(self, request):
        sheet_names = ['Sheet1', 'Data Sheet']
        headers = [['name', 'email', 'phone_number', 'date_of_birth', 'blood_group', 'city'], ['blood_group', 'city']]
        data_dict = {'Sheet1': [], 'Data Sheet': {'blood_group': Blood_Group.objects.all().values_list('name', flat=True), 'city': City.objects.all().values_list('name', flat=True)}}
        filename = 'donor_base_template.xlsx'
        column_widths = {'A': 30, 'B': 50, 'C': 40, 'D': 25, 'E': 20, 'F': 35}

        response = generate_excel_template(sheet_names, filename, headers, column_widths, data_dict = data_dict)
        return response
    
class DonorBulkImportAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @allowed_roles([RoleList.ADMIN.value])
    def post(self, request):
        try:
            excel_file = request.FILES["donors"]
        except:
            return CustomResponse(message="file not found").failure_reponse()
        if not excel_file.name.endswith('.xlsx'):
            return CustomResponse(message="file type not supported").failure_reponse()
        excel_data = get_excel_data(excel_file)
        
        headers = ['name', 'email', 'phone_number', 'date_of_birth', 'blood_group', 'city']
        if not excel_data:
            return CustomResponse(message="The file is empty.").failure_reponse()
        for header in headers:
            if header not in excel_data[0]:
                return CustomResponse(message=f"Please provide the {header} in the file.").failure_reponse()
        
        error_rows = []
        blood_groups_to_fetch = set()
        cities_to_fetch = set()
        for index, data in enumerate(excel_data[1:]):
            blood_group_name = data.get('blood_group')
            city_name = data.get('city')
            if not blood_group_name in blood_groups_to_fetch:
                if not Blood_Group.objects.filter(name=blood_group_name).exists():
                    error_rows.append({"row_index": index + 2, "error": "blood group does not exist"})
                blood_groups_to_fetch.add(blood_group_name)
            if not city_name in cities_to_fetch:
                if not City.objects.filter(name=city_name).exists():
                    error_rows.append({"row_index": index + 2, "error": "city does not exist"})
                cities_to_fetch.add(city_name)
        if error_rows:
            return CustomResponse(message="failed to import donors", data=error_rows).failure_reponse()
        
        blood_groups = Blood_Group.objects.filter(name__in=blood_groups_to_fetch).values('id', 'name')
        blood_group_name_to_id = {blood_group['name']: blood_group['id'] for blood_group in blood_groups}
        cities = City.objects.filter(name__in=cities_to_fetch).values('id', 'name')
        city_name_to_id = {city['name']: city['id'] for city in cities}
        for index, data in enumerate(excel_data[1:]):
            blood_group_name = data.pop('blood_group')
            city_name = data.pop('city')
            date_of_birth = data.pop('date_of_birth')
            blood_group_id = blood_group_name_to_id[blood_group_name]
            city_id = city_name_to_id[city_name]
            data['blood_group'] = blood_group_id
            data['city'] = city_id
            data['date_of_birth'] = date_of_birth.date()

        user_id = get_user_id(request)
        serializer = DonorCreateSerializer(data=excel_data[1:], context={'request': request, 'user_id': user_id}, many=True)
        with transaction.atomic():
            if serializer.is_valid():
                if len(serializer.data) != len(excel_data[1:]):
                    transaction.set_rollback(True)
                    return CustomResponse(message="something went wrong, please try again", data=serializer.errors).failure_reponse()
                serializer.save()
                return CustomResponse(message="successfully created donors", data=serializer.data).success_response()
        errors_with_indices = []
        for index, error in enumerate(serializer.errors):
            errors_with_indices.append({"row_index": index + 2, "error": error if error else "no error"})  # Adjust index for headers
        return CustomResponse(message="failed to import donors", data=errors_with_indices).failure_reponse()