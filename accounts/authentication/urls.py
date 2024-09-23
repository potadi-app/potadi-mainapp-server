from django.urls import path, include
from .oauth2.providers.google.views import GoogleLoginAPI
from .views import CustomRegistrationView, CustomLogoutView

urlpatterns = [
    # Custom logout
    path('logout/', CustomLogoutView.as_view(), name='rest_logout'),
    
    # Default dj_rest_auth URLs
    path('', include('dj_rest_auth.urls')),
    
    path('registration/', CustomRegistrationView.as_view(), name='custom-registration'),
    
    # Google OAuth login
    path('oauth2/google/', GoogleLoginAPI.as_view(), name="login-with-google"),
    
]
