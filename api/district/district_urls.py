from django.urls import path
from .district_view import DistrictAPIView, DistrictDropDownAPIView

urlpatterns = [
    path('', DistrictAPIView.as_view(), name='district_list'), #drop down
    path('all/', DistrictAPIView.as_view(), name='district_detail'), #get
    path('create/', DistrictAPIView.as_view(), name='district_create'), #single post

]