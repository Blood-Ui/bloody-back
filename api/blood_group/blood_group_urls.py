from django.urls import path
from .blood_group_view import Blood_Group_DropdownAPIview, Blood_Group_APIview

urlpatterns = [
        path('', Blood_Group_DropdownAPIview.as_view(), name='blood_group_list'), #drop down
        path('all/', Blood_Group_APIview.as_view(), name='blood_group_detail'), #get
        path('create/', Blood_Group_APIview.as_view(), name='blood_group_create'), #single post
        path('update/<uuid:blood_group_id>/', Blood_Group_APIview.as_view(), name='blood_group_update'), #single patch
        path('delete/<uuid:blood_group_id>/', Blood_Group_APIview.as_view(), name='blood_group_delete'), #single delete

    ]