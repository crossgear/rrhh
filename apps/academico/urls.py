from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DatosAcademicosViewSet

router = DefaultRouter()
router.register(r'datos-academicos', DatosAcademicosViewSet, basename='datos_academicos')

urlpatterns = [
    path('', include(router.urls)),
]
