from django.urls import path
from.views import RegisterUserView, VerifyUserEmail, LoginUserView,PasswordResetRequestView, PasswordResetConfirmView, SetNewPasswordView, LogoutUserView, TestAuthenticationView


urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('verify-email/', VerifyUserEmail.as_view(), name='verify-email'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('set-new-password/', SetNewPasswordView.as_view(), name='set-new-password'), 
    path('logout/', LogoutUserView.as_view(), name='logout'),

    path('test-authentication/', TestAuthenticationView.as_view(), name='test-authentication'),

]