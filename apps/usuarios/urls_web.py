"""
URLs web para autenticación de usuarios
"""
from django.urls import path
from .views_web import CustomLoginView, CustomLogoutView
from .views_admin import AdminRRHHListView, AdminRRHHCreateView, AdminRRHHDeleteView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path("administradores/", AdminRRHHListView.as_view(), name="admin-rrhh-list"),
    path("administradores/agregar/", AdminRRHHCreateView.as_view(), name="admin-rrhh-add"),
    path("administradores/<int:pk>/quitar/", AdminRRHHDeleteView.as_view(), name="admin-rrhh-delete"),
]
