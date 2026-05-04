
"""
Modelo Persona - Nodo principal del sistema
Todas las fichas laborales y académicas se vinculan a una Persona.
"""
from django.db import models
from django.conf import settings


class Persona(models.Model):
    """
    Modelo principal que contiene la información personal básica.
    Además incluye un JSON para almacenar la ficha ampliada que reemplaza el
    formulario en papel, manteniendo compatibilidad con la estructura original.
    """
    CI_NUMERO = models.CharField(
        'Número de CI',
        max_length=20,
        unique=True,
        help_text='Número de cédula de identidad único'
    )
    NOMBRES = models.CharField('Nombres', max_length=100)
    APELLIDOS = models.CharField('Apellidos', max_length=100)
    FECHA_NACIMIENTO = models.DateField('Fecha de nacimiento')

    ESTADO_CIVIL_CHOICES = [
        ('SOLTERO', 'Soltero/a'),
        ('CASADO', 'Casado/a'),
        ('DIVORCIADO', 'Divorciado/a'),
        ('VIUDO', 'Viudo/a'),
        ('UNION_LIBRE', 'Unión libre'),
    ]
    ESTADO_CIVIL = models.CharField(
        'Estado civil',
        max_length=20,
        choices=ESTADO_CIVIL_CHOICES,
        blank=True,
        default='SOLTERO'
    )

    USUARIO = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='persona',
        verbose_name='Usuario vinculado'
    )
    TELEFONO = models.CharField('Teléfono', max_length=20, blank=True)
    EMAIL = models.EmailField('Correo electrónico', blank=True)
    FOTO_CARNET = models.ImageField(
        'Foto carnet',
        upload_to='fotos_carnet/',
        blank=True,
        null=True,
    )
    FICHA_EXTRA = models.JSONField(
        'Datos ampliados de la ficha',
        default=dict,
        blank=True,
        help_text='Campos complementarios de la ficha web institucional'
    )

    ACTIVO = models.BooleanField('Activo', default=True)
    FECHA_CREACION = models.DateTimeField('Fecha de creación', auto_now_add=True)
    FECHA_ACTUALIZACION = models.DateTimeField('Última actualización', auto_now=True)

    class Meta:
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'
        ordering = ['APELLIDOS', 'NOMBRES']
        indexes = [
            models.Index(fields=['APELLIDOS', 'NOMBRES']),
            models.Index(fields=['CI_NUMERO']),
            models.Index(fields=['ACTIVO']),
        ]

    def __str__(self):
        return f"{self.NOMBRES} {self.APELLIDOS} - CI: {self.CI_NUMERO}"

    @property
    def nombre_completo(self):
        return f"{self.NOMBRES} {self.APELLIDOS}"

    @property
    def edad(self):
        from datetime import date
        today = date.today()
        return today.year - self.FECHA_NACIMIENTO.year - (
            (today.month, today.day) < (self.FECHA_NACIMIENTO.month, self.FECHA_NACIMIENTO.day)
        )

    @property
    def tiene_datos_laborales(self):
        return hasattr(self, 'datos_laborales') and self.datos_laborales is not None

    @property
    def tiene_datos_academicos(self):
        return hasattr(self, 'datos_academicos') and self.datos_academicos is not None

    @property
    def antiguedad_laboral(self):
        datos = getattr(self, 'datos_laborales', None)
        if datos and getattr(datos, 'antiguedad', ''):
            return datos.antiguedad
        return ''

    @property
    def antiguedad_origen(self):
        datos = getattr(self, 'datos_laborales', None)
        if datos and getattr(datos, 'antiguedad_origen', ''):
            return datos.antiguedad_origen
        return ''

    @property
    def antiguedad_run(self):
        datos = getattr(self, 'datos_laborales', None)
        if datos and getattr(datos, 'antiguedad_run', ''):
            return datos.antiguedad_run
        return ''

    @property
    def institucion_origen_label(self):
        datos = getattr(self, 'datos_laborales', None)
        if datos and getattr(datos, 'institucion_origen_label', ''):
            return datos.institucion_origen_label
        return 'Institución de origen'

