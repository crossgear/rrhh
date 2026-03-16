"""
Viewsets para Observacion
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Observacion
from .serializers import ObservacionSerializer
from apps.personas.models import Persona


class ObservacionViewSet(viewsets.ModelViewSet):
    """
    CRUD de observaciones.
    Solo RRHH y Admin pueden crear/modificar.
    """
    queryset = Observacion.objects.all()
    serializer_class = ObservacionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Observacion.objects.all().select_related('persona', 'usuario_creador')

    def perform_create(self, serializer):
        serializer.save(usuario_creador=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            # Solo admin puede modificar/eliminar (por auditoría)
            from apps.usuarios.permissions import IsAdminOrReadOnly
            permission_classes = [IsAdminOrReadOnly]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'])
    def por_persona(self, request):
        """Obtener observaciones de una persona."""
        persona_id = request.query_params.get('persona_id')
        if not persona_id:
            return Response(
                {'error': 'persona_id requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        queryset = self.get_queryset().filter(persona_id=persona_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def recientes(self, request):
        """Obtener las observaciones más recientes."""
        limite = request.query_params.get('limite', 50)
        try:
            limite = int(limite)
        except ValueError:
            limite = 50
        queryset = self.get_queryset()[:limite]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
