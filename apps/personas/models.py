"""
Modelo Persona - Nodo principal del sistema
Todas las fichas laborales y académicas se vinculan a una Persona.
"""
from django.db import models


class Persona(models.Model):
    """
    Modelo principal que contiene la información personal básica.
    Se relaciona con otros modelos mediante ForeignKey/OneToOne.
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

    TELEFONO = models.CharField('Teléfono', max_length=20, blank=True)
    EMAIL = models.EmailField('Correo electrónico', blank=True)

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
        """Retorna el nombre completo de la persona."""
        return f"{self.NOMBRES} {self.APELLIDOS}"

    @property
    def edad(self):
        """Calcula la edad actual."""
        from datetime import date
        today = date.today()
        return today.year - self.FECHA_NACIMIENTO.year - (
            (today.month, today.day) < (self.FECHA_NACIMIENTO.month, self.FECHA_NACIMIENTO.day)
        )

    @property
    def tiene_datos_laborales(self):
        """Verifica si tiene datos laborales registrados."""
        return hasattr(self, 'datos_laborales') and self.datos_laborales is not None

    @property
    def tiene_datos_academicos(self):
        """Verifica si tiene datos académicos registrados."""
        return hasattr(self, 'datos_academicos') and self.datos_academicos is not None
