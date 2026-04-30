"""
Modelo Observacion - Notas/observaciones sobre una persona
"""
from django.db import models
from apps.personas.models import Persona
from django.conf import settings


class Observacion(models.Model):
    """
    Modelo para registrar observaciones o notas sobre una persona.
    Incluye auditoría de quién creó la observación.
    """
    persona = models.ForeignKey(
        Persona,
        on_delete=models.CASCADE,
        related_name='observaciones',
        verbose_name='Persona'
    )
    usuario_creador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='observaciones_creadas',
        verbose_name='Creado por'
    )
    FECHA = models.DateTimeField('Fecha', auto_now_add=True)
    DESCRIPCION = models.TextField('Descripción')

    class Meta:
        verbose_name = 'Observación'
        verbose_name_plural = 'Observaciones'
        ordering = ['-FECHA']
        indexes = [
            models.Index(fields=['persona', '-FECHA']),
        ]

    def __str__(self):
        return f"{self.persona.nombre_completo} - {self.FECHA.strftime('%d/%m/%Y %H:%M')}"

    @property
    def autor_nombre(self):
        if self.usuario_creador:
            return self.usuario_creador.nombre_completo
        return 'Sistema'
