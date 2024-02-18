from django.urls import path
from .blood_group_view import Blood_Group_DropdownAPIview, Blood_Group_APIview, Blood_Group_Bulk_Import_APIview

urlpatterns = [
        path('', Blood_Group_DropdownAPIview.as_view(), name='blood_group_list'), #drop down
        path('all/', Blood_Group_APIview.as_view(), name='blood_group_detail'), #get
        path('create/', Blood_Group_APIview.as_view(), name='blood_group_create'), #single post
        path('update/<str:blood_group_id>/', Blood_Group_APIview.as_view(), name='blood_group_update'), #single patch
        path('delete/<str:blood_group_id>/', Blood_Group_APIview.as_view(), name='blood_group_delete'), #single delete

        path('bulk-import/', Blood_Group_Bulk_Import_APIview.as_view(), name='blood_group_bulk_import'), #bulk import

    ]