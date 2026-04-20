"""URLs de la app personas - API REST y Vistas Web"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PersonaViewSet
from .views_web import (
    PersonaListView,
    PersonaDetailView,
    PersonaCreateView,
    PersonaUpdateView,
    PersonaPrintView,
    MapaPersonasView,
    MiFichaView,
    MiFichaUpdateView,
    MiFichaPrintView,
)

router = DefaultRouter()
router.register(r'personas', PersonaViewSet, basename='persona-api')

urlpatterns = [
    path('api/', include(router.urls)),

    path('', PersonaListView.as_view(), name='persona-list'),
    path('crear/', PersonaCreateView.as_view(), name='persona-create'),
    path('mapa/', MapaPersonasView.as_view(), name='persona-mapa'),
    path('mi-ficha/', MiFichaView.as_view(), name='mi-ficha'),
    path('mi-ficha/editar/', MiFichaUpdateView.as_view(), name='mi-ficha-editar'),
    path('mi-ficha/imprimir/', MiFichaPrintView.as_view(), name='mi-ficha-print'),
    path('<int:pk>/', PersonaDetailView.as_view(), name='persona-detail'),
    path('<int:pk>/editar/', PersonaUpdateView.as_view(), name='persona-update'),
    path('<int:pk>/imprimir/', PersonaPrintView.as_view(), name='persona-print'),
]
