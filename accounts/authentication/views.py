from django.contrib.auth import logout as django_logout
from rest_framework.response import Response
from rest_framework import status
from django.dispatch import Signal
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LogoutView
from django.core.exceptions import ObjectDoesNotExist

user_logged_out = Signal()


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
