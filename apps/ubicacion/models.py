"""
Modelo Domicilio - Gestión de ubicaciones geográficas
Utiliza PostGIS PointField para almacenar coordenadas
"""
from django.contrib.gis.db import models as gis
from django.db import models
from apps.personas.models import Persona


class Domicilio(models.Model):
    """
    Modelo para almacenar domicilios de las personas.
    Soporta múltiples direcciones con historial (ES_ACTUAL marca la vigente).
    Incluye PointField para geoposicionamiento con SRID 4326 (WGS84).
    """
    persona = models.ForeignKey(
        Persona,
        on_delete=models.CASCADE,
        related_name='domicilios',
        verbose_name='Persona'
    )
    DIRECCION = models.CharField('Dirección', max_length=200)
    BARRIO = models.CharField('Barrio/Sector', max_length=100, blank=True)
    CIUDAD = models.CharField('Ciudad', max_length=100)

    # Campos para latitud/longitud decimales (fácil ingreso desde formulario)
    LATITUD = models.DecimalField(
        'Latitud',
        max_digits=10,
        decimal_places=8,
        blank=True,
        null=True,
        help_text='Coordenada en grados decimales'
    )
    LONGITUD = models.DecimalField(
        'Longitud',
        max_digits=11,
        decimal_places=8,
        blank=True,
        null=True,
        help_text='Coordenada en grados decimales'
    )

    # Campo GIS PointField - almacena geometría punto
    UBICACION = gis.PointField(
        'Ubicación geográfica',
        srid=4326,  # WGS84 - sistema de coordenadas GPS estándar
        blank=True,
        null=True,
        db_index=True
    )

    ES_ACTUAL = models.BooleanField('Dirección actual', default=True)
    FECHA_REGISTRO = models.DateTimeField('Fecha de registro', auto_now_add=True)

    class Meta:
        verbose_name = 'Domicilio'
        verbose_name_plural = 'Domicilios'
        ordering = ['-ES_ACTUAL', '-FECHA_REGISTRO']
        indexes = [
            models.Index(fields=['CIUDAD']),
            models.Index(fields=['ES_ACTUAL']),
            models.Index(fields=['persona', 'ES_ACTUAL']),
        ]

    def __str__(self):
        return f"{self.persona.nombre_completo} - {self.DIRECCION}, {self.CIUDAD}"

    def save(self, *args, **kwargs):
        """
        Sobrescribe save para crear PointField automáticamente
        desde lat/long si se proporcionan.
        """
        if self.LATITUD and self.LONGITUD:
            from django.contrib.gis.geos import Point
            # Point toma (longitud, latitud) - orden importante
            self.UBICACION = Point(float(self.LONGITUD), float(self.LATITUD))
        super().save(*args, **kwargs)

    @property
    def lat_long_str(self):
        """Retorna lat,long como string."""
        if self.LATITUD and self.LONGITUD:
            return f"{self.LATITUD}, {self.LONGITUD}"
        return "No definido"

    @property
    def coordenadas_dict(self):
        """Retorna dict con coordenadas."""
        if self.LATITUD and self.LONGITUD:
            return {
                'lat': float(self.LATITUD),
                'lng': float(self.LONGITUD)
            }
        return None
