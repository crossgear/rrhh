"""
Serializers para el modelo Persona
"""
from rest_framework import serializers
from django.db.models import Q
from .models import Persona


class PersonaSerializer(serializers.ModelSerializer):
    """
    Serializer para lectura y escritura de Persona.
    """
    nombre_completo = serializers.CharField(source='nombre_completo', read_only=True)
    edad = serializers.IntegerField(read_only=True)
    tiene_datos_laborales = serializers.BooleanField(read_only=True)
    tiene_datos_academicos = serializers.BooleanField(read_only=True)

    class Meta:
        model = Persona
        fields = [
            'id',
            'CI_NUMERO',
            'NOMBRES',
            'APELLIDOS',
            'FECHA_NACIMIENTO',
            'edad',
            'ESTADO_CIVIL',
            'TELEFONO',
            'EMAIL',
            'ACTIVO',
            'FECHA_CREACION',
            'FECHA_ACTUALIZACION',
            'nombre_completo',
            'tiene_datos_laborales',
            'tiene_datos_academicos',
        ]
        read_only_fields = [
            'id',
            'FECHA_CREACION',
            'FECHA_ACTUALIZACION',
            'edad',
            'nombre_completo',
            'tiene_datos_laborales',
            'tiene_datos_academicos',
        ]

    def validate_CI_NUMERO(self, value):
        """Validar que la cédula sea única."""
        if value:
            qs = Persona.objects.filter(CI_NUMERO=value)
            if self.instance:
                qs = qs.exclude(id=self.instance.id)
            if qs.exists():
                raise serializers.ValidationError('Esta cédula ya está registrada.')
        return value

    def validate_EMAIL(self, value):
        """Validar formato de email si se proporciona."""
        if value:
            # Django ya valida el formato, aquí podríamos agregar reglas adicionales
            pass
        return value


class PersonaSearchSerializer(serializers.Serializer):
    """
    Serializer para búsqueda de personas.
    """
    query = serializers.CharField(required=True, min_length=3)
    tipo = serializers.ChoiceField(
        choices=['nombre', 'apellido', 'ci', 'email', 'telefono'],
        required=False,
        default='nombre'
    )
