from django.urls import path, include
from .views import CustomRegistrationView, CustomLogoutView, SocialAccountListView

urlpatterns = [
    # Custom logout
    path('logout/', CustomLogoutView.as_view(), name='rest_logout'),
    
    # Default dj_rest_auth URLs
    path('', include('dj_rest_auth.urls')),
    
    path('registration/', CustomRegistrationView.as_view(), name='custom-registration'),
    
    # OAuth login
    path('oauth/status/', SocialAccountListView.as_view(), name="social-accounts-list"),
    
    path('oauth/google/', include('accounts.authentication.oauth.providers.google.urls')),
    
]
