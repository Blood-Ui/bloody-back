from django.urls import path
from .patient_view import PatientAPIView, PatientDropDownAPIView

urlpatterns = [
    path('', PatientDropDownAPIView.as_view(), name='patient_list'), #drop down
    path('all/', PatientAPIView.as_view(), name='patient_detail'), #get
    path('create/', PatientAPIView.as_view(), name='patient_create'), #single post
    path('update/<str:patient_id>/', PatientAPIView.as_view(), name='patient_update'), #single patch
    path('delete/<str:patient_id>/', PatientAPIView.as_view(), name='patient_delete'), #single delete
    
]