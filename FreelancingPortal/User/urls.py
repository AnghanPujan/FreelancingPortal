from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView 
from .views import (
    RegisterAPIView, 
    LoginTokenObtainPairAPIView, 
    LogoutAPIView,
    ChangePasswordView
)

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='user_register'),
    path('login/', LoginTokenObtainPairAPIView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutAPIView.as_view(), name='user_logout'),
    path("change-password/", ChangePasswordView.as_view(), name="change_password")
]