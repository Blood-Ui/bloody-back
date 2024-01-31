from django.urls import path
from blood_group_view import Blood_Group_DropdownAPIView

urlpatterns = [
        path('', Blood_Group_DropdownAPIView.as_view(), name='blood_group_list'), #drop down
        path('all/', Blood_Group_DropdownAPIView.as_view(), name='blood_group_detail'), #get

    ]