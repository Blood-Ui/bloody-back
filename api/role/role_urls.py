from django.urls import path
from .role_view import RoleDropDownAPIView, RoleAPIView, UserRoleView

urlpatterns = [
        path('', RoleDropDownAPIView.as_view(), name='role_list'), #drop down
        path('all/', RoleAPIView.as_view(), name='role_detail'), #get
        path('create/', RoleAPIView.as_view(), name='role_create'), #single post
        path('update/<str:role_id>/', RoleAPIView.as_view(), name='role_update'), #single patch
        path('delete/<str:role_id>/', RoleAPIView.as_view(), name='role_delete'), #single delete

        path('user-role/', UserRoleView.as_view(), name='user-role'), #get
        path('user-role/create/', UserRoleView.as_view(), name='user-role-create'), #single post
        path('user-role/update/<str:user_role_id>/', UserRoleView.as_view(), name='user-role-update'), #single patch
        path('user-role/delete/<str:user_role_id>/', UserRoleView.as_view(), name='user-role-delete'), #single delete

    ]