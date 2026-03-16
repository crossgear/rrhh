"""
URLs web para autenticación de usuarios
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import UsuarioViewSet  # Para perfil API

urlpatterns = [
    # Login
    path('login/', auth_views.LoginView.as_view(
        template_name='usuarios/login.html',
        redirect_authenticated_user=True
    ), name='login'),

    # Logout
    path('logout/', auth_views.LogoutView.as_view(
        next_page='login'
    ), name='logout'),

    # API para perfil de usuario
    # Esta ruta es para API, se maneja desde views_web o views
]
