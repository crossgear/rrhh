"""
Viewsets para DatosLaborales
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import DatosLaborales
from .serializers import DatosLaboralesSerializer
from apps.personas.models import Persona


class DatosLaboralesViewSet(viewsets.ModelViewSet):
    """
    CRUD de datos laborales.
    """
    queryset = DatosLaborales.objects.all()
    serializer_class = DatosLaboralesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DatosLaborales.objects.all().select_related('persona')

    @action(detail=False, methods=['get'])
    def por_persona(self, request):
        """Obtener datos laborales por persona."""
        persona_id = request.query_params.get('persona_id')
        if not persona_id:
            return Response(
                {'error': 'persona_id requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            datos = self.get_queryset().get(persona_id=persona_id)
            serializer = self.get_serializer(datos)
            return Response(serializer.data)
        except DatosLaborales.DoesNotExist:
            return Response(
                {'error': 'No encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['get'])
    def activos(self, request):
        """Listar solo datos laborales de personas activas."""
        queryset = self.get_queryset().filter(ACTIVO=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def por_dependencia(self, request):
        """Agrupar por dependencia."""
        from django.db.models import Count
        datos = self.get_queryset().values('DEPENDENCIA').annotate(total=Count('id')).order_by('DEPENDENCIA')
        return Response(datos)
