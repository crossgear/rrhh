"""
Viewsets para Domicilio
Incluye vista especial para GeoJSON del mapa
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q

from .models import Domicilio
from .serializers import DomicilioSerializer, DomicilioGeoSerializer, DomicilioCreateUpdateSerializer


class DomicilioViewSet(viewsets.ModelViewSet):
    """
    CRUD completo de domicilios.
    """
    queryset = Domicilio.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return DomicilioCreateUpdateSerializer
        return DomicilioSerializer

    def get_queryset(self):
        """
        Optimiza queries con select_related.
        """
        return Domicilio.objects.all().select_related('persona')

    def perform_create(self, serializer):
        """
        Si se crea un domicilio como actual, desactivar otros de la misma persona.
        """
        instance = serializer.save()
        if instance.ES_ACTUAL:
            Domicilio.objects.filter(
                persona=instance.persona,
                ES_ACTUAL=True
            ).exclude(id=instance.id).update(ES_ACTUAL=False)

    def perform_update(self, serializer):
        """
        Si se marca como actual, desactivar otros.
        """
        instance = serializer.save()
        if instance.ES_ACTUAL:
            Domicilio.objects.filter(
                persona=instance.persona,
                ES_ACTUAL=True
            ).exclude(id=instance.id).update(ES_ACTUAL=False)

    @action(detail=False, methods=['get'])
    def por_persona(self, request):
        """
        Listar domicilios de una persona específica.
        GET /api/ubicacion/domicilios/por_persona/?persona_id=X
        """
        persona_id = request.query_params.get('persona_id')
        if not persona_id:
            return Response(
                {'error': 'Parámetro persona_id requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        queryset = self.get_queryset().filter(persona_id=persona_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def actuales(self, request):
        """
        Listar solo domicilios actuales (vigentes).
        """
        queryset = self.get_queryset().filter(ES_ACTUAL=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def por_ciudad(self, request):
        """
        Filtrar domicilios por ciudad.
        GET /api/ubicacion/domicilios/por_ciudad/?ciudad=Asunción
        """
        ciudad = request.query_params.get('ciudad')
        if not ciudad:
            return Response(
                {'error': 'Parámetro ciudad requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        queryset = self.get_queryset().filter(CIUDAD__iexact=ciudad)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class MapaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Vista de solo lectura para obtener domicilios en formato GeoJSON
    para ser consumidos por mapas (Leaflet, OpenLayers, etc.).
    """
    queryset = Domicilio.objects.filter(ES_ACTUAL=True, UBICACION__isnull=False).select_related('persona')
    serializer_class = DomicilioGeoSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        """
        Permite filtrar por ciudad desde query params.
        """
        queryset = super().get_queryset().filter(UBICACION__isnull=False)
        ciudad = self.request.query_params.get('CIUDAD')
        if ciudad:
            queryset = queryset.filter(CIUDAD__iexact=ciudad)
        return queryset
