"""
URLs de la app personas - API REST y Vistas Web
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PersonaViewSet
from .views_web import (
    PersonaListView,
    PersonaDetailView,
    PersonaCreateView,
    PersonaUpdateView,
    MapaPersonasView,
)

# API Router
router = DefaultRouter()
router.register(r'personas', PersonaViewSet, basename='persona-api')

urlpatterns = [
    # API REST
    path('api/', include(router.urls)),

    # Vistas web
    path('', PersonaListView.as_view(), name='persona-list'),
    path('<int:pk>/', PersonaDetailView.as_view(), name='persona-detail'),
    path('crear/', PersonaCreateView.as_view(), name='persona-create'),
    path('<int:pk>/editar/', PersonaUpdateView.as_view(), name='persona-update'),
    path('mapa/', MapaPersonasView.as_view(), name='persona-mapa'),
]
