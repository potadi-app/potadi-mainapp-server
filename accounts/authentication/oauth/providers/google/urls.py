from django.urls import path
from .views import GoogleLoginAPI, GoogleConnectView, GoogleDisconnectAPI

urlpatterns = [
    # Google OAuth login
    path('', GoogleLoginAPI.as_view(), name="socialaccount_login"),
    path('connect/', GoogleConnectView.as_view(), name="socialaccount_connections"),
    path('disconnect/<int:pk>/', GoogleDisconnectAPI.as_view(), name="socialaccount_disconnect"),
]
