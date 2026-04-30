"""
Viewsets para Familiar
"""
from rest_framework import viewsets, permissions
from .models import Familiar
from .serializers import FamiliarSerializer


class FamiliarViewSet(viewsets.ModelViewSet):
    queryset = Familiar.objects.all()
    serializer_class = FamiliarSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Familiar.objects.all().select_related('persona')
