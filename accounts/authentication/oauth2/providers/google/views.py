from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from accounts.authentication.utils import generate_tokens_for_user, get_user_data, get_or_create_user

class GoogleLoginAPI(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_OAUTH_CALLBACK_URL
    client_class = OAuth2Client
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = request.user
        
        if user.is_authenticated:
            user_data = get_user_data(user)
            
            if user_data:
                user = get_or_create_user(user_data)
                access_token, refresh_token = generate_tokens_for_user(user)
                response_data = {
                    'user': user_data,
                    'access': access_token,
                    'refresh': refresh_token
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'error': 'Social account not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        return response
