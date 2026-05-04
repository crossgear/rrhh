from __future__ import annotations

from decimal import Decimal
from datetime import date, datetime
from typing import Any

from .models import Auditoria


def _normalize(value: Any):
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if isinstance(value, dict):
        return {k: _normalize(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_normalize(v) for v in value]
    return value


def registrar_auditoria(*, usuario, accion: str, modelo: str, objeto_id=None, objeto_repr='', descripcion='', antes=None, despues=None):
    Auditoria.objects.create(
        usuario=usuario if getattr(usuario, 'is_authenticated', False) else None,
        accion=accion,
        modelo=modelo,
        objeto_id=str(objeto_id) if objeto_id is not None else None,
        objeto_repr=objeto_repr or '',
        descripcion=descripcion or '',
        datos_antes=_normalize(antes),
        datos_despues=_normalize(despues),
    )
