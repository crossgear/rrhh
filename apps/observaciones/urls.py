from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ObservacionViewSet
from .views_web import ObservacionCreateView

router = DefaultRouter()
router.register(r'observaciones', ObservacionViewSet, basename='observacion')

urlpatterns = [
    # API REST
    path('api/', include(router.urls)),
    # Vistas web
    path('crear/', ObservacionCreateView.as_view(), name='observacion-crear'),
]
