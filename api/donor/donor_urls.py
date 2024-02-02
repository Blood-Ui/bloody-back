from django.urls import path
from.donor_view import DonorAPIView

urlpatterns = [
    path('all/', DonorAPIView.as_view(), name='donor_detail'), #get
    path('create/', DonorAPIView.as_view(), name='donor_create'), #single post
    path('update/<uuid:donor_id>/', DonorAPIView.as_view(), name='donor_update'), #single patch
    path('delete/<uuid:donor_id>/', DonorAPIView.as_view(), name='donor_delete'), #single delete

]