from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from api.models import Patient, Request
from api.utils import CustomResponse, get_user_id, get_user_role
from .patient_serializer import PatientCreateSerializer, PatientListSerializer, PatientDropDownSerializer, PatientUpdateSerializer, RequestListSerializer, RequestUpdateSerializer


class PatientAPIView(APIView):
    permission_classes = [IsAuthenticated]

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
    
    def get(self, request):
        print(get_user_role(request))
        patients = Patient.objects.all()
        serializer = PatientListSerializer(patients, many=True)
        return CustomResponse(message="successfully obtained patients", data=serializer.data).success_response()
    
    def delete(self, request, patient_id):
        if not Patient.objects.filter(id=patient_id).exists():
            return CustomResponse(message="patient does not exist").failure_reponse()
        patient = Patient.objects.filter(id=patient_id).first()
        patient.delete()
        return CustomResponse(message="successfully deleted patient").success_response()
    
class PatientDropDownAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        patients = Patient.objects.all()
        serializer = PatientDropDownSerializer(patients, many=True)
        return CustomResponse(message="successfully obtained patients", data=serializer.data).success_response()
    
class RequestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        requests = Request.objects.all()
        serializer = RequestListSerializer(requests, many=True)
        return CustomResponse(message="successfully obtained requests", data=serializer.data).success_response()
    
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