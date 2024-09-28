from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView, SocialConnectView, SocialAccountDisconnectView
from rest_framework import status
from rest_framework.response import Response
from django.utils.translation import gettext as _
from django.conf import settings

class GoogleLoginAPI(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_OAUTH_CALLBACK_URL
    client_class = OAuth2Client
    
class GoogleConnectView(SocialConnectView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_OAUTH_CALLBACK_URL
    client_class = OAuth2Client
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == status.HTTP_200_OK:
            # Override response message
            return Response({'detail': _('Connected with Google account')}, status=status.HTTP_200_OK)
            
        return response

class GoogleDisconnectAPI(SocialAccountDisconnectView):
    adapter_class = GoogleOAuth2Adapter
    
    def post(self, request, pk, *args, **kwargs):
        accounts = self.get_queryset()
        account = accounts.filter(provider='google', id=pk).first()

        if account:
            account.delete()
            return Response({'detail': _('Social account disconnected.')})
        else:
            return Response({'detail': _('Social account not found.')},
                            status=status.HTTP_400_BAD_REQUEST)
