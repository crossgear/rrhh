"""
Serializers para DatosAcademicos
"""
from rest_framework import serializers
from .models import DatosAcademicos


class DatosAcademicosSerializer(serializers.ModelSerializer):
    persona_nombre = serializers.SerializerMethodField()
    persona_ci = serializers.SerializerMethodField()
    nivel_mostrar = serializers.SerializerMethodField()

    class Meta:
        model = DatosAcademicos
        fields = [
            'id',
            'persona',
            'persona_nombre',
            'persona_ci',
            'NIVEL_ACADEMICO',
            'nivel_mostrar',
            'PROFESION',
            'UNIVERSIDAD',
            'ANIO_GRADUACION',
            'TIENE_POSTGRADO',
            'TIENE_MAESTRIA',
            'TIENE_DOCTORADO',
            'FECHA_CREACION',
            'FECHA_ACTUALIZACION',
        ]
        read_only_fields = ['id', 'FECHA_CREACION', 'FECHA_ACTUALIZACION', 'nivel_mostrar']

    def get_persona_nombre(self, obj):
        return obj.persona.nombre_completo

    def get_persona_ci(self, obj):
        return obj.persona.CI_NUMERO

    def get_nivel_mostrar(self, obj):
        return obj.nivel_maximo
