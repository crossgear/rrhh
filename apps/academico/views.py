"""
Viewsets para DatosAcademicos
"""
from rest_framework import viewsets, permissions
from .models import DatosAcademicos
from .serializers import DatosAcademicosSerializer


class DatosAcademicosViewSet(viewsets.ModelViewSet):
    queryset = DatosAcademicos.objects.all()
    serializer_class = DatosAcademicosSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DatosAcademicos.objects.all().select_related('persona')
