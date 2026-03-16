"""
Serializers para Observacion
"""
from rest_framework import serializers
from django.conf import settings
from .models import Observacion


class ObservacionSerializer(serializers.ModelSerializer):
    persona_nombre = serializers.SerializerMethodField()
    usuario_nombre = serializers.SerializerMethodField()

    class Meta:
        model = Observacion
        fields = [
            'id',
            'persona',
            'persona_nombre',
            'usuario_creador',
            'usuario_nombre',
            'FECHA',
            'DESCRIPCION',
        ]
        read_only_fields = ['id', 'FECHA', 'usuario_creador']

    def get_persona_nombre(self, obj):
        return obj.persona.nombre_completo

    def get_usuario_nombre(self, obj):
        return obj.autor_nombre

    def create(self, validated_data):
        """
        Asignar automáticamente el usuario creador.
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['usuario_creador'] = request.user
        return super().create(validated_data)

    def validate_DESCRIPCION(self, value):
        """Validar que la descripción no esté vacía y tenga longitud mínima."""
        if not value or not value.strip():
            raise serializers.ValidationError('La descripción no puede estar vacía.')
        if len(value.strip()) < 10:
            raise serializers.ValidationError('La descripción debe tener al menos 10 caracteres.')
        return value.strip()
