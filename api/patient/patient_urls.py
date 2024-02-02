from django.urls import path
from .patient_view import PatientAPIView

urlpatterns = [
    path('all/', PatientAPIView.as_view(), name='patient_detail'), #get
    path('create/', PatientAPIView.as_view(), name='patient_create'), #single post
    path('update/<uuid:patient_id>/', PatientAPIView.as_view(), name='patient_update'), #single patch
    path('delete/<uuid:patient_id>/', PatientAPIView.as_view(), name='patient_delete'), #single delete
]