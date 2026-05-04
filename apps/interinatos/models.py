from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.personas.models import Persona


def resolucion_interinato_upload_to(instance, filename):
    ci = instance.persona.CI_NUMERO if instance.persona_id else 'sin-ci'
    return f'interinatos/{ci}/{timezone.now():%Y/%m}/{filename}'


class Interinato(models.Model):
    persona = models.ForeignKey(
        Persona,
        on_delete=models.CASCADE,
        related_name='interinatos',
        verbose_name='Funcionario',
    )
    cargo_interino = models.CharField('Cargo interino', max_length=180)
    dependencia = models.CharField('Dependencia / área', max_length=180, blank=True, default='')
    numero_resolucion = models.CharField('N° de resolución', max_length=80)
    fecha_resolucion = models.DateField('Fecha de resolución', blank=True, null=True)
    fecha_inicio = models.DateField('Inicio de interinato')
    fecha_fin = models.DateField('Fin de interinato')
    archivo_resolucion = models.FileField(
        'Resolución en PDF',
        upload_to=resolucion_interinato_upload_to,
        help_text='Adjunte la resolución en formato PDF.',
    )
    observacion = models.TextField('Observación', blank=True, default='')
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='interinatos_creados',
        verbose_name='Cargado por',
    )
    fecha_creacion = models.DateTimeField('Fecha de creación', auto_now_add=True)
    fecha_actualizacion = models.DateTimeField('Última actualización', auto_now=True)

    class Meta:
        verbose_name = 'Interinato'
        verbose_name_plural = 'Interinatos'
        ordering = ['-fecha_inicio', '-fecha_creacion']
        indexes = [
            models.Index(fields=['fecha_inicio', 'fecha_fin']),
            models.Index(fields=['numero_resolucion']),
        ]

    def __str__(self):
        return f'{self.persona.nombre_completo} - {self.cargo_interino}'

    @property
    def estado(self):
        hoy = timezone.localdate()
        if hoy < self.fecha_inicio:
            return 'PENDIENTE'
        if hoy > self.fecha_fin:
            return 'FINALIZADO'
        return 'VIGENTE'

    @property
    def estado_display(self):
        return {
            'PENDIENTE': 'Pendiente',
            'VIGENTE': 'Vigente',
            'FINALIZADO': 'Finalizado',
        }.get(self.estado, self.estado)

    @property
    def estado_badge(self):
        return {
            'PENDIENTE': 'warning',
            'VIGENTE': 'success',
            'FINALIZADO': 'secondary',
        }.get(self.estado, 'secondary')
