from django.urls import path
from .district_view import DistrictAPIView, DistrictDropDownAPIView, DistrictBaseTemplateAPIView, DistrictBulkImportAPIView

urlpatterns = [
    path('', DistrictDropDownAPIView.as_view(), name='district_list'), #drop down
    path('all/', DistrictAPIView.as_view(), name='district_detail'), #get
    path('create/', DistrictAPIView.as_view(), name='district_create'), #single post
    path('update/<str:district_id>/', DistrictAPIView.as_view(), name='district_update'), #single patch
    path('delete/<str:district_id>/', DistrictAPIView.as_view(), name='district_delete'), #single delete

    path('base-template/', DistrictBaseTemplateAPIView.as_view(), name='district_base_template'), #get
    path('bulk-import/', DistrictBulkImportAPIView.as_view(), name='district_bulk_import'), #bulk post

]