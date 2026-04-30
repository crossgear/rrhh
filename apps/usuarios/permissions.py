"""
Permisos personalizados para el sistema RRHH
"""
from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permite lectura a cualquier usuario autenticado.
    Solo permite escritura a administradores (ADMIN).
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.ROL == 'ADMIN'


class IsRRHHOrAdmin(permissions.BasePermission):
    """
    Permite acceso solo a usuarios con rol ADMIN o RRHH.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.ROL in ['ADMIN', 'RRHH']
        )


class IsOwnerOrRRHH(permissions.BasePermission):
    """
    Permite acceso al dueño del recurso o a RRHH/Admin.
    Útil para observaciones o datos personales.
    """
    def has_object_permission(self, request, view, obj):
        # RRHH y Admin tienen acceso completo
        if request.user.ROL in ['ADMIN', 'RRHH']:
            return True
        # De lo contrario, solo el dueño
        return obj.usuario_creador == request.user


class CanViewPersona(permissions.BasePermission):
    """
    Permiso específico para ver fichas de personal.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated
