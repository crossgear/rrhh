from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FamiliarViewSet

router = DefaultRouter()
router.register(r'familiares', FamiliarViewSet, basename='familiar')

urlpatterns = [
    path('', include(router.urls)),
]
