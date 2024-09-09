from django.urls import path, include
from .oauth2.providers.google.views import GoogleLoginAPI

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('oauth2/google/', GoogleLoginAPI.as_view(), name="login-with-google"),
]
