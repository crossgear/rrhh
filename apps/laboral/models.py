
"""
Modelo DatosLaborales - Información laboral del funcionario
"""
from django.db import models
from apps.personas.models import Persona


class DatosLaborales(models.Model):
    persona = models.OneToOneField(
        Persona,
        on_delete=models.CASCADE,
        related_name='datos_laborales',
        verbose_name='Persona'
    )

    TIPO_VINCULO_CHOICES = [
        ('NOMBRADO', 'Nombrado/a'),
        ('CONTRATADO', 'Contratado/a'),
        ('PASANTIA', 'Pasantía'),
        ('PRACTICANTE', 'Practicante'),
        ('OTRO', 'Otro'),
    ]
    TIPO_VINCULO = models.CharField(
        'Tipo de vínculo',
        max_length=20,
        choices=TIPO_VINCULO_CHOICES,
        blank=True,
        default='OTRO'
    )

    INSTITUCION = models.CharField(
        'Institución',
        max_length=100,
        default='Corte Suprema de Justicia',
        help_text='Institución donde trabaja'
    )
    DEPENDENCIA = models.CharField(
        'Dependencia / Lugar de trabajo',
        max_length=150,
        blank=True,
        default=''
    )
    CARGO = models.CharField('Cargo', max_length=150, blank=True, default='')

    NUMERO_DECRETO = models.CharField('N° Decreto', max_length=50, blank=True, default='')
    FECHA_DECRETO = models.DateField('Fecha de decreto', blank=True, null=True)

    NUMERO_RESOLUCION = models.CharField('N° Resolución', max_length=50, blank=True, default='')
    FECHA_RESOLUCION = models.DateField('Fecha de resolución', blank=True, null=True)

    SALARIO = models.DecimalField(
        'Salario',
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        help_text='Salario en G. (guaraníes)'
    )
    ACTIVO = models.BooleanField('Activo', default=True)
    FECHA_INGRESO = models.DateField('Fecha de ingreso', blank=True, null=True)
    FECHA_CREACION = models.DateTimeField('Fecha de creación', auto_now_add=True)
    FECHA_ACTUALIZACION = models.DateTimeField('Última actualización', auto_now=True)

    class Meta:
        verbose_name = 'Datos Laborales'
        verbose_name_plural = 'Datos Laborales'
        ordering = ['-FECHA_INGRESO']
        indexes = [
            models.Index(fields=['TIPO_VINCULO']),
            models.Index(fields=['ACTIVO']),
            models.Index(fields=['DEPENDENCIA']),
        ]

    def __str__(self):
        return f"{self.persona.nombre_completo} - {self.CARGO or 'Sin cargo'} ({self.DEPENDENCIA or 'Sin dependencia'})"
