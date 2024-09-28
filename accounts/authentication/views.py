from django.contrib.auth import logout as django_logout
from rest_framework.response import Response
from rest_framework import status
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LogoutView
from django.core.exceptions import ObjectDoesNotExist
from dj_rest_auth.registration.views import SocialAccountListView as _SocialAccountListView

class SocialAccountListView(_SocialAccountListView):
    def get(self, request, *args, **kwargs):
        accounts = self.get_queryset()
        response = []
        
        for account in accounts:
            email = account.extra_data.get('email') if account.extra_data else None
            last_login = account.user.last_login if account.user else None
            date_joined = account.user.date_joined if account.user else None
            
            response.append({
                'id': account.id,
                'provider': account.provider,
                'uid': account.uid,
                'email': email,
                'last_login': last_login,
                'date_joined': date_joined,
                # 'extra_data': account.extra_data,
            })
        
        return Response(response)

class CustomLogoutView(LogoutView):
    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        django_logout(request)

        response = Response({"detail": "Successfully logged out."},
                            status=status.HTTP_200_OK)

        # Hapus semua cookie yang mungkin ada
        for cookie in request.COOKIES:
            response.delete_cookie(cookie)
            
        return response

class CustomRegistrationView(RegisterView):
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        response.data.pop('access', None)
        response.data.pop('refresh', None)

        return response
