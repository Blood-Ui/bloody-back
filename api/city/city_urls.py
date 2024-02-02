from django.urls import path
from .city_view import CityAPIView, CityDropDownView

urlpatterns = [
    path('', CityDropDownView.as_view(), name='city_list'), #drop down
    path('all/', CityAPIView.as_view(), name='city_detail'), #get
    path('create/', CityAPIView.as_view(), name='city_create'), #single post
    path('update/<str:city_id>/', CityAPIView.as_view(), name='city_update'), #single patch
    path('delete/<str:city_id>/', CityAPIView.as_view(), name='city_delete'), #single delete
    
]