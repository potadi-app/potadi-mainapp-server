from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DiagnoseViewSetAPI

router = DefaultRouter()
router.register(r'', DiagnoseViewSetAPI, basename='diagnose')

urlpatterns = [
    path('', include(router.urls)),
]