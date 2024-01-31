from django.urls import path
from .role_view import RoleDropDownAPIView, RoleAPIView, UserRoleView

urlpatterns = [
        path('', RoleDropDownAPIView.as_view(), name='role_list'),
        path('all/', RoleAPIView.as_view(), name='role_detail'), #get
        path('create/', RoleAPIView.as_view(), name='role_create'), #single post
        path('update/<uuid:role_id>/', RoleAPIView.as_view(), name='role_update'), #single patch
        path('delete/<uuid:role_id>/', RoleAPIView.as_view(), name='role_delete'), #single delete

        path('user-role/', UserRoleView.as_view(), name='user-role'), #get
        path('user-role/create/', UserRoleView.as_view(), name='user-role-create'),

    ]
