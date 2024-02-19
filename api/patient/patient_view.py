from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from api.models import Patient, Request, Blood_Group, City
from api.utils import CustomResponse, get_user_id, RoleList, allowed_roles, get_excel_data, generate_excel_template
from .patient_serializer import PatientCreateSerializer, PatientListSerializer, PatientDropDownSerializer, PatientUpdateSerializer, RequestListSerializer, RequestUpdateSerializer


class PatientAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @allowed_roles([RoleList.ADMIN.value])
    def post(self, request):
        user_id = get_user_id(request)
        serializer = PatientCreateSerializer(data=request.data, context={"request": request, "user_id": user_id})
        with transaction.atomic():
            request_created = False
            if serializer.is_valid():
                serializer.save()
                if Request.objects.filter(patient_id=serializer.data['id']).exists() :
                    request_created = True
                    return CustomResponse(message={"message": "successfully created patient", "request_created": request_created}, data=serializer.data).success_response()
                else:
                    transaction.set_rollback(True)
                    return CustomResponse(message={"message": "failed to create patient", "response": "request was not generated", "request_created": request_created}, data=serializer.errors).failure_reponse()
            return CustomResponse(message={"message": "failed to create patient", "request_created": request_created}, data=serializer.errors).failure_reponse()

    @allowed_roles([RoleList.ADMIN.value])
    def patch(self, request, patient_id):
        user_id = get_user_id(request)
        if not Patient.objects.filter(id=patient_id).exists():
            return CustomResponse(message="patient does not exist").failure_reponse()
        patient = Patient.objects.filter(id=patient_id).first()
        serializer = PatientUpdateSerializer(patient, data=request.data, context={"request": request, "user_id": user_id}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(message="successfully updated patient", data=serializer.data).success_response()
        return CustomResponse(message="failed to update patient", data=serializer.errors).failure_reponse()
    
    @allowed_roles([RoleList.ADMIN.value])
    def get(self, request):
        patients = Patient.objects.all()
        serializer = PatientListSerializer(patients, many=True)
        return CustomResponse(message="successfully obtained patients", data=serializer.data).success_response()
    
    @allowed_roles([RoleList.ADMIN.value])
    def delete(self, request, patient_id):
        if not Patient.objects.filter(id=patient_id).exists():
            return CustomResponse(message="patient does not exist").failure_reponse()
        patient = Patient.objects.filter(id=patient_id).first()
        patient.delete()
        return CustomResponse(message="successfully deleted patient").success_response()
    
class PatientDropDownAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @allowed_roles([RoleList.ADMIN.value])
    def get(self, request):
        patients = Patient.objects.all()
        serializer = PatientDropDownSerializer(patients, many=True)
        return CustomResponse(message="successfully obtained patients", data=serializer.data).success_response()
    
class RequestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @allowed_roles([RoleList.ADMIN.value])
    def get(self, request):
        requests = Request.objects.all()
        serializer = RequestListSerializer(requests, many=True)
        return CustomResponse(message="successfully obtained requests", data=serializer.data).success_response()
    
    @allowed_roles([RoleList.ADMIN.value])
    def patch(self, request, request_id):
        user_id = get_user_id(request)
        if not Request.objects.filter(id=request_id).exists():
            return CustomResponse(message="request does not exist").failure_reponse()
        patient_request = Request.objects.filter(id=request_id).first()
        serializer = RequestUpdateSerializer(patient_request, data=request.data, context={"request": request, "user_id": user_id}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(message="successfully updated request", data=serializer.data).success_response()
        return CustomResponse(message="failed to update request", data=serializer.errors).failure_reponse()
    
class PatientBaseTemplateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @allowed_roles([RoleList.ADMIN.value])
    def get(self, request):
        sheet_names = ['Sheet1', 'Data Sheet']
        headers = [['name', 'bystander_name', 'bystander_phone_number', 'hospital_name', 'blood_group', 'city'], ['blood_group', 'city']]
        data_dict = {'Sheet1': [], 'Data Sheet': {'blood_group': Blood_Group.objects.all().values_list('name', flat=True), 'city': City.objects.all().values_list('name', flat=True)}}
        filename = 'patient_base_template.xlsx'
        column_widths = {'A': 30, 'B': 30, 'C': 30, 'D': 40, 'E': 20, 'F': 35}

        response = generate_excel_template(sheet_names, filename, headers, column_widths, data_dict)
        return response
    
class PatientBulkImportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @allowed_roles([RoleList.ADMIN.value])
    def post(self, request):
        try:
            excel_file = request.FILES["patients"]
        except:
            return CustomResponse(message="file not found").failure_reponse()
        if not excel_file.name.endswith('.xlsx'):
            return CustomResponse(message="file type not supported").failure_reponse()
        excel_data = get_excel_data(excel_file)
        
        headers = ['name', 'bystander_name', 'bystander_phone_number', 'hospital_name', 'blood_group', 'city']
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
            blood_group_id = blood_group_name_to_id[blood_group_name]
            city_id = city_name_to_id[city_name]
            data['blood_group'] = blood_group_id
            data['city'] = city_id

        user_id = get_user_id(request)
        serializer = PatientCreateSerializer(data=excel_data[1:], context={'request': request, 'user_id': user_id}, many=True)
        with transaction.atomic():
            if serializer.is_valid():
                if len(serializer.data) != len(excel_data[1:]):
                    transaction.set_rollback(True)
                    return CustomResponse(message="something went wrong, please try again", data=serializer.errors).failure_reponse()
                serializer.save()
                return CustomResponse(message="successfully imported patients", data=serializer.data).success_response()
        errors_with_indices = []
        for index, error in enumerate(serializer.errors):
            errors_with_indices.append({"row_index": index + 2, "error": error if error else "no error"})  # Adjust index for headers
        return CustomResponse(message="failed to import patients", data=errors_with_indices).failure_reponse()    
