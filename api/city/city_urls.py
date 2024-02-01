from django.urls import path
from .city_view import CityAPIView

urlpatterns = [
    path('create/', CityAPIView.as_view(), name='city_create'), #single post
]