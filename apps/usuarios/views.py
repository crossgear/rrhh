"""
Viewsets para el modelo Usuario
"""
from rest_framework import viewsets, permissions, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models import Q

from .models import Usuario
from .serializers import UsuarioSerializer, UsuarioCreateSerializer, ChangePasswordSerializer
from .permissions import IsAdminOrReadOnly, IsRRHHOrAdmin

Usuario = get_user_model()


class UsuarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar usuarios.
    - Admin ve todos los usuarios
    - RRHH ve usuarios activos
    - Consulta solo ve su propio perfil
    """
    queryset = Usuario.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return UsuarioCreateSerializer
        return UsuarioSerializer

    def get_permissions(self):
        """
        Permisos dinámicos según acción:
        - list/retrieve: Permisos por rol
        - create/update/delete: Solo ADMIN
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminOrReadOnly]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Filtrado de usuarios por rol:
        - ADMIN: todos
        - RRHH: solo activos
        - CONSULTA: solo el propio usuario
        """
        user = self.request.user
        queryset = Usuario.objects.all()

        if not user.is_authenticated:
            return Usuario.objects.none()

        if user.ROL == Usuario.Rol.ADMIN:
            return queryset
        elif user.ROL == Usuario.Rol.RRHH:
            return queryset.filter(is_active=True)
        else:
            return queryset.filter(id=user.id)

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    @action(detail=False, methods=['get'])
    def perfil(self, request):
        """Endpoint para obtener el perfil del usuario actual."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def cambiar_password(self, request):
        """Endpoint para cambiar contraseña del usuario actual."""
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response(
                    {'error': 'Contraseña actual incorrecta'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'mensaje': 'Contraseña actualizada exitosamente'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def por_rol(self, request):
        """Listar usuarios filtrados por rol."""
        rol = request.query_params.get('rol')
        if rol:
            queryset = self.get_queryset().filter(ROL=rol)
        else:
            queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def empleados_activos(self, request):
        """Listar empleados activos (útil para selectores)."""
        queryset = self.get_queryset().filter(is_active=True).order_by('last_name', 'first_name')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
