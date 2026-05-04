from django.conf import settings
from django.db import models
from datetime import datetime
from decimal import Decimal, InvalidOperation



FIELD_LABELS = {
    'ci_numero': 'C.I. N°',
    'nombres': 'Nombres',
    'apellidos': 'Apellidos',
    'telefono': 'Teléfono',
    'email': 'Correo institucional',
    'activo': 'Funcionario activo',
    'celular': 'Celular',
    'ciudad': 'Ciudad',
    'barrio': 'Barrio',
    'domicilio_actual': 'Domicilio actual',
    'tipo_vinculo': 'Tipo de vínculo',
    'cargo': 'Cargo',
    'dependencia': 'Lugar de trabajo',
    'salario': 'Salario',
    'fecha_ingreso': 'Fecha de ingreso',
    'funcionario': 'Funcionario',
    'cargo_interino': 'Cargo interino',
    'numero_resolucion': 'N° de resolución',
    'fecha_resolucion': 'Fecha de resolución',
    'fecha_inicio': 'Inicio de interinato',
    'fecha_fin': 'Fin de interinato',
    'archivo_resolucion': 'Resolución PDF',
    'observacion': 'Observación',
    'estado': 'Estado',
}


def _format_money(value):
    if value in (None, ''):
        return '-'
    raw = str(value).replace('.', '').replace(',', '')
    if not raw:
        return '-'
    try:
        number = int(Decimal(raw))
    except (InvalidOperation, ValueError):
        return str(value)
    return f"{number:,}".replace(',', '.')


def _format_value(field, value):
    if value in (None, '', []):
        return '-'
    if field == 'activo':
        return 'Sí' if value in (True, 'True', 'true', '1', 1) else 'No'
    if field == 'salario':
        return _format_money(value)
    if field in ('fecha_ingreso', 'fecha_resolucion', 'fecha_inicio', 'fecha_fin'):
        try:
            return datetime.fromisoformat(str(value)).strftime('%d/%m/%Y')
        except Exception:
            return str(value)
    return str(value)



class Auditoria(models.Model):
    class Accion(models.TextChoices):
        CREAR = 'CREAR', 'Crear'
        EDITAR = 'EDITAR', 'Editar'
        ELIMINAR = 'ELIMINAR', 'Eliminar'

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='auditorias')
    accion = models.CharField(max_length=12, choices=Accion.choices)
    modelo = models.CharField(max_length=100)
    objeto_id = models.CharField(max_length=50, blank=True, null=True)
    objeto_repr = models.CharField(max_length=255, blank=True)
    descripcion = models.TextField(blank=True)
    datos_antes = models.JSONField(blank=True, null=True)
    datos_despues = models.JSONField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    @property
    def detalle_cambios(self):
        antes = self.datos_antes or {}
        despues = self.datos_despues or {}
        if not isinstance(antes, dict):
            antes = {}
        if not isinstance(despues, dict):
            despues = {}

        cambios = []
        campos = list(dict.fromkeys([*antes.keys(), *despues.keys()]))
        for campo in campos:
            valor_antes = antes.get(campo)
            valor_despues = despues.get(campo)
            if self.accion == self.Accion.EDITAR and valor_antes == valor_despues:
                continue
            cambios.append({
                'campo': campo,
                'label': FIELD_LABELS.get(campo, campo.replace('_', ' ').capitalize()),
                'antes': _format_value(campo, valor_antes),
                'despues': _format_value(campo, valor_despues),
            })
        return cambios

    @property
    def resumen_cambios(self):
        """Resumen corto y amigable para mostrar en la tabla principal."""
        cambios = self.detalle_cambios

        if self.accion == self.Accion.EDITAR:
            if not cambios:
                return 'No se detectaron cambios detallados.'
            nombres = [c.get('label', c.get('campo', 'Campo')) for c in cambios]
            primeros = ', '.join(nombres[:3])
            restantes = len(nombres) - 3
            if restantes > 0:
                primeros = f"{primeros} y {restantes} más"
            return f"Modificó {len(nombres)} campo(s): {primeros}."

        if self.accion == self.Accion.CREAR:
            return 'Registró un nuevo interinato.' if self.modelo == 'Interinato' else 'Registró una nueva ficha.'

        if self.accion == self.Accion.ELIMINAR:
            return 'Eliminó un interinato registrado.' if self.modelo == 'Interinato' else 'Eliminó una ficha registrada.'

        return self.descripcion or '-'



    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Auditoría'
        verbose_name_plural = 'Auditoría'
        indexes = [
            models.Index(fields=['accion']),
            models.Index(fields=['modelo']),
            models.Index(fields=['fecha']),
        ]

    def __str__(self):
        usuario = getattr(self.usuario, 'username', 'sistema')
        return f"{self.fecha:%d/%m/%Y %H:%M} - {usuario} - {self.accion} - {self.modelo}"
