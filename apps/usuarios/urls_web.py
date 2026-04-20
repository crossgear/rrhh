"""
URLs web para autenticación de usuarios
"""
from django.urls import path
from .views_web import CustomLoginView, CustomLogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]
