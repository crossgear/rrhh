"""
Modelo Familiar - Familiares del funcionario
"""
from django.db import models
from apps.personas.models import Persona


class Familiar(models.Model):
    """
    Modelo para registrar familiares de la persona.
    """
    persona = models.ForeignKey(
        Persona,
        on_delete=models.CASCADE,
        related_name='familiares',
        verbose_name='Persona'
    )

    TIPO_CHOICES = [
        ('PADRE', 'Padre'),
        ('MADRE', 'Madre'),
        ('CONYUGE', 'Cónyuge'),
        ('HIJO', 'Hijo/a'),
        ('HERMANO', 'Hermano/a'),
        ('OTRO', 'Otro'),
    ]
    TIPO = models.CharField('Tipo de familiar', max_length=20, choices=TIPO_CHOICES)
    NOMBRE = models.CharField('Nombre', max_length=100)
    APELLIDO = models.CharField('Apellido', max_length=100)
    FECHA_NACIMIENTO = models.DateField('Fecha de nacimiento', blank=True, null=True)
    VIVE = models.BooleanField('Vive', default=True)
    TELEFONO = models.CharField('Teléfono', max_length=20, blank=True)

    class Meta:
        verbose_name = 'Familiar'
        verbose_name_plural = 'Familiares'
        ordering = ['TIPO', 'APELLIDO', 'NOMBRE']

    def __str__(self):
        return f"{self.NOMBRE} {self.APELLIDO} ({self.get_TIPO_display()})"

    @property
    def nombre_completo(self):
        return f"{self.NOMBRE} {self.APELLIDO}"
