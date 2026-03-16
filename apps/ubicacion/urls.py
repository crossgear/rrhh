"""
URLs de la app ubicacion - API REST y GeoJSON
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DomicilioViewSet, MapaViewSet

router = DefaultRouter()
router.register(r'domicilios', DomicilioViewSet, basename='domicilio')

urlpatterns = [
    path('', include(router.urls)),
    # Ruta específica para mapa GeoJSON
    path('mapa/', MapaViewSet.as_view({'get': 'list'}), name='mapa-list'),
]
