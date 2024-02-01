from django.urls import path
from .district_view import DistrictAPIView

urlpatterns = [
    path('all/', DistrictAPIView.as_view(), name='district_detail'), #get
    path('create/', DistrictAPIView.as_view(), name='district_create'), #single post

]