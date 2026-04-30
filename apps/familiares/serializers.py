"""
Serializers para Familiar
"""
from rest_framework import serializers
from .models import Familiar


class FamiliarSerializer(serializers.ModelSerializer):
    persona_nombre = serializers.SerializerMethodField()
    tipo_display = serializers.CharField(source='get_TIPO_display', read_only=True)

    class Meta:
        model = Familiar
        fields = [
            'id',
            'persona',
            'persona_nombre',
            'TIPO',
            'tipo_display',
            'NOMBRE',
            'APELLIDO',
            'FECHA_NACIMIENTO',
            'VIVE',
            'TELEFONO',
        ]
        read_only_fields = ['id']

    def get_persona_nombre(self, obj):
        return obj.persona.nombre_completo
