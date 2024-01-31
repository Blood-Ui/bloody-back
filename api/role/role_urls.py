from django.urls import path
from .role_view import RoleDropDownAPIView, RoleAPIView

urlpatterns = [
        path('', RoleDropDownAPIView.as_view(), name='role_list'),

    ]
