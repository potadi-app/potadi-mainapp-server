from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from urllib.parse import urlencode

v1_schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="Documentation API for Potadi App",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="potadi.ai@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

def api_docs_view(request):
    """Handle redirection to swagger or redoc based on query parameter, default to redoc"""
    doc_type = request.GET.get('v')
    
    if not doc_type:
        # If 'v' parameter is not present, redirect to the same URL with 'v=swagger'
        query_params = urlencode({'v': 'swagger'})
        redirect_url = f"{request.path}?{query_params}"
        return HttpResponseRedirect(redirect_url)
    
    if doc_type == 'swagger':
        return v1_schema_view.with_ui('swagger', cache_timeout=0)(request)
    elif doc_type == 'redoc':
        return v1_schema_view.with_ui('redoc', cache_timeout=0)(request)
    else:
        return HttpResponseBadRequest("Invalid query parameter. Use 'v=swagger' or 'v=redoc'.")

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API Documentation Route with version and query parameter
    re_path(r'^v1/docs/$', api_docs_view, name='api-docs'),

    # Apps Routes
    path('v1/auth/', include('accounts.authentication.urls')),
    path('v1/diagnose/', include('diagnose.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
