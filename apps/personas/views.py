"""
Viewsets para el modelo Persona
"""
from rest_framework import viewsets, permissions, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend

from .models import Persona
from .serializers import PersonaSerializer


class PersonaViewSet(viewsets.ModelViewSet):
    """
    ViewSet completo para gestionar personas.
    Incluye búsqueda, filtrado y acciones personalizadas.
    """
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend, 'rest_framework.filters.SearchFilter', 'rest_framework.filters.OrderingFilter']
    filterset_fields = ['ACTIVO', 'ESTADO_CIVIL']
    search_fields = ['CI_NUMERO', 'NOMBRES', 'APELLIDOS', 'TELEFONO', 'EMAIL']
    ordering_fields = ['APELLIDOS', 'NOMBRES', 'FECHA_NACIMIENTO', 'FECHA_CREACION']
    ordering = ['APELLIDOS', 'NOMBRES']

    def get_queryset(self):
        """
        Optimiza queries con select_related.
        """
        return Persona.objects.all()

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    @action(detail=False, methods=['get'])
    def activas(self, request):
        """Listar solo personas activas."""
        queryset = self.get_queryset().filter(ACTIVO=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def inactivas(self, request):
        """Listar solo personas inactivas."""
        queryset = self.get_queryset().filter(ACTIVO=False)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def buscar_por_ci(self, request):
        """Búsqueda rápida por CI."""
        ci = request.query_params.get('ci')
        if not ci:
            return Response(
                {'error': 'Parámetro "ci" requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            persona = Persona.objects.get(CI_NUMERO=ci)
            serializer = self.get_serializer(persona)
            return Response(serializer.data)
        except Persona.DoesNotExist:
            return Response(
                {'error': 'Persona no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['get'])
    def perfil_completo(self, request, pk=None):
        """
        Devuelve el perfil completo de una persona,
        incluyendo datos laborales, académicos, familiares, etc.
        """
        persona = self.get_object()
        data = PersonaSerializer(persona).data

        # Agregar datos laborales si existen
        if hasattr(persona, 'datos_laborales'):
            from apps.laboral.serializers import DatosLaboralesSerializer
            data['datos_laborales'] = DatosLaboralesSerializer(persona.datos_laborales).data

        # Agregar datos académicos si existen
        if hasattr(persona, 'datos_academicos'):
            from apps.academico.serializers import DatosAcademicosSerializer
            data['datos_academicos'] = DatosAcademicosSerializer(persona.datos_academicos).data

        # Agregar domicilios
        from apps.ubicacion.serializers import DomicilioSerializer
        domicilios = persona.domicilios.all()
        data['domicilios'] = DomicilioSerializer(domicilios, many=True).data

        # Agregar familiares
        from apps.familiares.serializers import FamiliarSerializer
        familiares = persona.familiares.all()
        data['familiares'] = FamiliarSerializer(familiares, many=True).data

        # Agregar observaciones
        from apps.observaciones.serializers import ObservacionSerializer
        observaciones = persona.observaciones.all()
        data['observaciones'] = ObservacionSerializer(observaciones, many=True).data

        return Response(data)
