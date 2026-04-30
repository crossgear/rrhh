from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DatosLaboralesViewSet

router = DefaultRouter()
router.register(r'datos-laborales', DatosLaboralesViewSet, basename='datos_laborales')

urlpatterns = [
    path('', include(router.urls)),
]
