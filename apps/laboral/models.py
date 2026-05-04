"""
Modelo DatosLaborales - Información laboral del funcionario
"""
from django.db import models
from apps.personas.models import Persona
from datetime import date

FECHA_CORTE_ORIGEN = date(2025, 12, 31)
FECHA_INICIO_RUN = date(2026, 1, 1)


def formatear_periodo(fecha_inicio, fecha_fin=None):
    """Devuelve un período legible entre dos fechas: X años y Y meses."""
    if not fecha_inicio:
        return ''
    fecha_fin = fecha_fin or date.today()
    if fecha_fin < fecha_inicio:
        return ''

    years = fecha_fin.year - fecha_inicio.year
    months = fecha_fin.month - fecha_inicio.month
    if fecha_fin.day < fecha_inicio.day:
        months -= 1
    if months < 0:
        years -= 1
        months += 12

    if years <= 0:
        return f"{months} mes{'es' if months != 1 else ''}" if months > 0 else 'Menos de 1 mes'
    if months <= 0:
        return f"{years} año{'s' if years != 1 else ''}"
    return f"{years} año{'s' if years != 1 else ''} y {months} mes{'es' if months != 1 else ''}"


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
        ('COMISIONADO', 'Comisionado/a'),
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

    INSTITUCION_ORIGEN_CHOICES = [
        ('RUN', 'Registro Unificado Nacional'),
        ('MEF', 'Ministerio de Economía y Finanzas'),
        ('DGRP', 'Dirección General de los Registros Públicos'),
        ('DAG', 'Departamento de Agrimensura y Geodesia'),
        ('OTRO', 'Otra institución'),
    ]
    INSTITUCION_ORIGEN = models.CharField(
        'Institución de origen',
        max_length=10,
        choices=INSTITUCION_ORIGEN_CHOICES,
        blank=True,
        default='RUN',
        help_text='Institución de origen o institución actual RUN para funcionarios ingresados desde el 01/01/2026'
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

    INSTITUCION_DESTINO_COMISION = models.CharField(
        'Institución de destino en comisión',
        max_length=150,
        blank=True,
        default='',
        help_text='Entidad donde presta servicios temporalmente el funcionario comisionado.'
    )
    NUMERO_RESOLUCION_COMISION = models.CharField('N° Resolución / autorización de comisión', max_length=50, blank=True, default='')
    FECHA_INICIO_COMISION = models.DateField('Fecha inicio comisión', blank=True, null=True)
    FECHA_FIN_COMISION = models.DateField('Fecha fin comisión', blank=True, null=True)
    OBSERVACION_COMISION = models.TextField('Observación comisión', blank=True, default='')

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
            models.Index(fields=['INSTITUCION_ORIGEN']),
            models.Index(fields=['ACTIVO']),
            models.Index(fields=['DEPENDENCIA']),
        ]

    def __str__(self):
        return f"{self.persona.nombre_completo} - {self.CARGO or 'Sin cargo'} ({self.DEPENDENCIA or 'Sin dependencia'})"

    def save(self, *args, **kwargs):
        """Garantiza consistencia institucional.

        Los ingresos desde el 01/01/2026 se asignan al RUN, salvo funcionarios
        comisionados, porque ellos conservan una institución de origen externa.
        """
        if self.FECHA_INGRESO and self.FECHA_INGRESO >= FECHA_INICIO_RUN and self.TIPO_VINCULO != 'COMISIONADO':
            self.INSTITUCION_ORIGEN = 'RUN'
        super().save(*args, **kwargs)

    @property
    def antiguedad(self):
        """Devuelve la antigüedad total legible desde FECHA_INGRESO hasta hoy."""
        return formatear_periodo(self.FECHA_INGRESO)

    @property
    def antiguedad_origen(self):
        """
        Antigüedad acumulada en la institución de origen hasta el 31/12/2025.
        Aplica para funcionarios que venían del MEF, DGRP, DAG u otra institución
        antes de la unificación al RUN.
        """
        if not self.FECHA_INGRESO or self.FECHA_INGRESO >= FECHA_INICIO_RUN:
            return ''
        return formatear_periodo(self.FECHA_INGRESO, FECHA_CORTE_ORIGEN)

    @property
    def antiguedad_run(self):
        """Antigüedad en el Registro Unificado Nacional desde el 01/01/2026."""
        if not self.FECHA_INGRESO:
            return ''
        inicio = max(self.FECHA_INGRESO, FECHA_INICIO_RUN)
        return formatear_periodo(inicio)

    @property
    def periodo_comision(self):
        if not self.FECHA_INICIO_COMISION and not self.FECHA_FIN_COMISION:
            return ''
        inicio = self.FECHA_INICIO_COMISION.strftime('%d/%m/%Y') if self.FECHA_INICIO_COMISION else 'Sin inicio'
        fin = self.FECHA_FIN_COMISION.strftime('%d/%m/%Y') if self.FECHA_FIN_COMISION else 'Sin fin'
        return f'{inicio} al {fin}'

    @property
    def institucion_origen_label(self):
        """Etiqueta legible para mostrar la institución anterior al RUN."""
        if getattr(self, 'INSTITUCION_ORIGEN', ''):
            return self.get_INSTITUCION_ORIGEN_display()
        nombre = (self.INSTITUCION or '').upper()
        if 'RUN' in nombre or 'REGISTRO UNIFICADO' in nombre:
            return 'Registro Unificado Nacional'
        if 'ECONOM' in nombre or 'MEF' in nombre:
            return 'Ministerio de Economía y Finanzas'
        if 'REGISTROS' in nombre or 'DGRP' in nombre:
            return 'Dirección General de los Registros Públicos'
        if 'AGRIMENSURA' in nombre or 'GEODESIA' in nombre or 'DAG' in nombre:
            return 'Departamento de Agrimensura y Geodesia'
        return 'Institución de origen'
