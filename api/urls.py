from django.urls import path, include

urlpatterns = [
    path('role/', include('api.role.role_urls')),
    
]