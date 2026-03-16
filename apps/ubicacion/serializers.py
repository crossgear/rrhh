"""
Serializers para el modelo Domicilio
Incluye serializer GeoJSON para mapas
"""
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Domicilio


class DomicilioSerializer(serializers.ModelSerializer):
    """
    Serializer estándar para Domicilio.
    """
    persona_nombre = serializers.SerializerMethodField()
    persona_ci = serializers.SerializerMethodField()
    lat_long = serializers.SerializerMethodField()

    class Meta:
        model = Domicilio
        fields = [
            'id',
            'persona',
            'persona_nombre',
            'persona_ci',
            'DIRECCION',
            'BARRIO',
            'CIUDAD',
            'LATITUD',
            'LONGITUD',
            'lat_long',
            'ES_ACTUAL',
            'FECHA_REGISTRO',
        ]
        read_only_fields = ['id', 'FECHA_REGISTRO']

    def get_persona_nombre(self, obj):
        return obj.persona.nombre_completo

    def get_persona_ci(self, obj):
        return obj.persona.CI_NUMERO

    def get_lat_long(self, obj):
        return obj.lat_long_str

    def validate(self, data):
        """
        Validar que si hay lat/long, se cree PointField.
        """
        lat = data.get('LATITUD')
        lon = data.get('LONGITUD')
        if (lat and not lon) or (lon and not lat):
            raise serializers.ValidationError(
                'Debe proporcionar tanto latitud como longitud o ninguna.'
            )
        return data

    def create(self, validated_data):
        instance = Domicilio.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class DomicilioGeoSerializer(GeoFeatureModelSerializer):
    """
    Serializer especializado para GeoJSON.
    """
    persona_nombre = serializers.SerializerMethodField()
    persona_ci = serializers.SerializerMethodField()

    class Meta:
        model = Domicilio
        geo_field = 'UBICACION'
        fields = [
            'id',
            'persona',
            'persona_nombre',
            'persona_ci',
            'DIRECCION',
            'BARRIO',
            'CIUDAD',
            'ES_ACTUAL',
            'FECHA_REGISTRO',
        ]
        auto_bbox = True

    def get_persona_nombre(self, obj):
        return obj.persona.nombre_completo

    def get_persona_ci(self, obj):
        return obj.persona.CI_NUMERO

    def get_properties(self, obj, fields):
        """
        Personalizar las propiedades del GeoJSON.
        """
        properties = super().get_properties(obj, fields)
        # Agregar propiedades extra para el popup
        properties['popup_html'] = f"""
            <strong>{obj.persona.nombre_completo}</strong><br>
            CI: {obj.persona.CI_NUMERO}<br>
            {obj.DIRECCION}<br>
            {obj.BARRIO if obj.BARRIO else ''}<br>
            {obj.CIUDAD}
        """
        return properties


class DomicilioCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para crear/actualizar domicilios
    con envío de lat/long desde frontend.
    """
    class Meta:
        model = Domicilio
        fields = [
            'id',
            'persona',
            'DIRECCION',
            'BARRIO',
            'CIUDAD',
            'LATITUD',
            'LONGITUD',
            'ES_ACTUAL',
        ]
        read_only_fields = ['id']

    def validate(self, data):
        lat = data.get('LATITUD')
        lon = data.get('LONGITUD')
        if lat is not None and lon is None or lon is not None and lat is None:
            raise serializers.ValidationError(
                'Debe proporcionar latitud y longitud juntos.'
            )
        if lat and lon:
            if not (-90 <= lat <= 90):
                raise serializers.ValidationError('Latitud debe estar entre -90 y 90')
            if not (-180 <= lon <= 180):
                raise serializers.ValidationError('Longitud debe estar entre -180 y 180')
        return data
