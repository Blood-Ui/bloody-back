from django.urls import path, include

urlpatterns = [
    path('role/', include('api.role.role_urls')),
    path('blood-group/', include('api.blood_group.blood_group_urls')),
    path('district/', include('api.district.district_urls')),
    
]