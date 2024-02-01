from django.urls import path
from .district_view import DistrictAPIView

urlpatterns = [
    path('create/', DistrictAPIView.as_view(), name='district_create'), #single post
    
]