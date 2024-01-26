from django.urls import path
from.views import RegisterUserView, VerifyUserEmail


urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('verify-email/', VerifyUserEmail.as_view(), name='verify-email'),
]