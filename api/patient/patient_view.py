from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db import transaction

from api.models import Patient, Request
from .patient_serializer import PatientCreateSerializer, PatientListSerializer, PatientDropDownSerializer, PatientUpdateSerializer


class PatientAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)
        if response is not None:
            # unpacking
            user , token = response
            user_id = token.payload['user_id']

        serializer = PatientCreateSerializer(data=request.data, context={"request": request, "user_id": user_id})
        with transaction.atomic():
            request_created = False
            if serializer.is_valid():
                serializer.save()
                if Request.objects.filter(patient_id=serializer.data['id']).exists() :
                    request_created = True
                    return Response({"message": "successfully created patient", "response": serializer.data, "request_created": request_created}, status=status.HTTP_201_CREATED)
                else:
                    transaction.set_rollback(True)
                    return Response({"message": "failed to create patient", "response": "request was not generated", "request_created": request_created}, status=status.HTTP_201_CREATED)
            return Response({"message": "failed to create patient", "response": serializer.errors, "request_created": request_created}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, patient_id):
        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)
        if response is not None:
            # unpacking
            user , token = response
            user_id = token.payload['user_id']
        
        if not Patient.objects.filter(id=patient_id).exists():
            return Response({"message": "patient does not exist"}, status=status.HTTP_404_NOT_FOUND)
        patient = Patient.objects.filter(id=patient_id).first()
        serializer = PatientUpdateSerializer(patient, data=request.data, context={"request": request, "user_id": user_id}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "successfully updated patient", "response": serializer.data}, status=status.HTTP_200_OK)
        return Response({"message": "failed to update patient", "response": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        patients = Patient.objects.all()
        serializer = PatientListSerializer(patients, many=True)
        return Response({"message": "successfully retrieved patients", "response": serializer.data}, status=status.HTTP_200_OK)
    
    def delete(self, request, patient_id):
        if not Patient.objects.filter(id=patient_id).exists():
            return Response({"message": "patient does not exist"}, status=status.HTTP_404_NOT_FOUND)
        patient = Patient.objects.filter(id=patient_id).first()

        patient.delete()
        return Response({"message": "successfully deleted patient"}, status=status.HTTP_200_OK)
    
class PatientDropDownAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        patients = Patient.objects.all()
        serializer = PatientDropDownSerializer(patients, many=True)
        return Response({"message": "successfully retrieved patients", "response": serializer.data}, status=status.HTTP_200_OK)