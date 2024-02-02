from django.urls import path
from.donor_view import DonorAPIView

urlpatterns = [
    path('create/', DonorAPIView.as_view(), name='donor_create'), #single post

]