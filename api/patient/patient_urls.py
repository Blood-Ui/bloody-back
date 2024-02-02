from django.urls import path
from .patient_view import PatientAPIView

urlpatterns = [
    path('create/', PatientAPIView.as_view(), name='patient_create'), #single post
]