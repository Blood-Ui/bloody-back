from django.urls import path
from .city_view import CityAPIView, CityDropDownView, CityBulkImportAPIView, CityBaseTemplateAPIView

urlpatterns = [
    path('drop-down/<str:district_id>/', CityDropDownView.as_view(), name='city_list'), #drop down
    path('all/', CityAPIView.as_view(), name='city_detail'), #get
    path('create/', CityAPIView.as_view(), name='city_create'), #single post
    path('update/<str:city_id>/', CityAPIView.as_view(), name='city_update'), #single patch
    path('delete/<str:city_id>/', CityAPIView.as_view(), name='city_delete'), #single delete
    
    path('base-template/', CityBaseTemplateAPIView.as_view(), name='city_base_template'), #base template
    path('bulk-import/', CityBulkImportAPIView.as_view(), name='city_bulk_import'), #bulk post
]