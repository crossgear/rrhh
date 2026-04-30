
"""
Modelo DatosAcademicos - Información académica del funcionario
"""
from django.db import models
from apps.personas.models import Persona


class DatosAcademicos(models.Model):
    persona = models.OneToOneField(
        Persona,
        on_delete=models.CASCADE,
        related_name='datos_academicos',
        verbose_name='Persona'
    )

    NIVEL_ACADEMICO_CHOICES = [
        ('NINGUNO', 'No especificado'),
        ('PRIMARIO', 'Primario'),
        ('SECUNDARIO', 'Secundario'),
        ('UNIVERSITARIO', 'Universitario'),
        ('POSTGRADO', 'Postgrado'),
        ('MAESTRIA', 'Maestría'),
        ('DOCTORADO', 'Doctorado'),
    ]
    NIVEL_ACADEMICO = models.CharField(
        'Nivel académico',
        max_length=20,
        choices=NIVEL_ACADEMICO_CHOICES,
        blank=True,
        default='NINGUNO'
    )

    PROFESION = models.CharField('Profesión/Carrera', max_length=150, blank=True, help_text='Ej: Derecho, Contabilidad, etc.')
    UNIVERSIDAD = models.CharField('Universidad', max_length=150, blank=True, help_text='Institución donde estudió')
    ANIO_GRADUACION = models.PositiveIntegerField('Año de graduación', blank=True, null=True)

    TIENE_POSTGRADO = models.BooleanField('Tiene postgrado', default=False)
    TIENE_MAESTRIA = models.BooleanField('Tiene maestría', default=False)
    TIENE_DOCTORADO = models.BooleanField('Tiene doctorado', default=False)

    FECHA_CREACION = models.DateTimeField('Fecha de creación', auto_now_add=True)
    FECHA_ACTUALIZACION = models.DateTimeField('Última actualización', auto_now=True)

    class Meta:
        verbose_name = 'Datos Académicos'
        verbose_name_plural = 'Datos Académicos'
        indexes = [models.Index(fields=['NIVEL_ACADEMICO'])]

    def __str__(self):
        return f"{self.persona.nombre_completo} - {self.get_NIVEL_ACADEMICO_display()}"

    @property
    def nivel_maximo(self):
        if self.TIENE_DOCTORADO:
            return 'DOCTORADO'
        if self.TIENE_MAESTRIA:
            return 'MAESTRIA'
        if self.TIENE_POSTGRADO:
            return 'POSTGRADO'
        return self.NIVEL_ACADEMICO
