"""
Serializers para DatosLaborales
"""
from rest_framework import serializers
from .models import DatosLaborales


class DatosLaboralesSerializer(serializers.ModelSerializer):
    """Serializer para DatosLaborales."""
    persona_nombre = serializers.SerializerMethodField()
    persona_ci = serializers.SerializerMethodField()
    tipo_vinculo_display = serializers.CharField(source='get_TIPO_VINCULO_display', read_only=True)

    class Meta:
        model = DatosLaborales
        fields = [
            'id',
            'persona',
            'persona_nombre',
            'persona_ci',
            'TIPO_VINCULO',
            'tipo_vinculo_display',
            'INSTITUCION',
            'DEPENDENCIA',
            'CARGO',
            'NUMERO_DECRETO',
            'FECHA_DECRETO',
            'NUMERO_RESOLUCION',
            'FECHA_RESOLUCION',
            'INSTITUCION_DESTINO_COMISION',
            'NUMERO_RESOLUCION_COMISION',
            'FECHA_INICIO_COMISION',
            'FECHA_FIN_COMISION',
            'OBSERVACION_COMISION',
            'SALARIO',
            'ACTIVO',
            'FECHA_INGRESO',
            'FECHA_CREACION',
            'FECHA_ACTUALIZACION',
        ]
        read_only_fields = ['id', 'FECHA_CREACION', 'FECHA_ACTUALIZACION']

    def get_persona_nombre(self, obj):
        return obj.persona.nombre_completo

    def get_persona_ci(self, obj):
        return obj.persona.CI_NUMERO

    def validate_SALARIO(self, value):
        if value < 0:
            raise serializers.ValidationError('El salario no puede ser negativo')
        return value
