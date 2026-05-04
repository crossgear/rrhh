"""
Admin para DatosLaborales
"""
from django.contrib import admin
from .models import DatosLaborales


@admin.register(DatosLaborales)
class DatosLaboralesAdmin(admin.ModelAdmin):
    list_display = (
        'persona',
        'TIPO_VINCULO',
        'CARGO',
        'DEPENDENCIA',
        'SALARIO',
        'ACTIVO',
        'FECHA_INGRESO'
    )
    list_filter = ('TIPO_VINCULO', 'INSTITUCION_ORIGEN', 'ACTIVO', 'DEPENDENCIA')
    search_fields = (
        'persona__NOMBRES',
        'persona__APELLIDOS',
        'persona__CI_NUMERO',
        'CARGO',
        'DEPENDENCIA'
    )
    ordering = ('-FECHA_INGRESO',)
    readonly_fields = ('FECHA_CREACION', 'FECHA_ACTUALIZACION')

    fieldsets = (
        ('Persona', {
            'fields': ('persona',)
        }),
        ('Vinculación', {
            'fields': ('TIPO_VINCULO', 'INSTITUCION_ORIGEN', 'INSTITUCION', 'DEPENDENCIA', 'CARGO')
        }),
        ('Documentación', {
            'fields': ('NUMERO_DECRETO', 'FECHA_DECRETO', 'NUMERO_RESOLUCION', 'FECHA_RESOLUCION', 'INSTITUCION_DESTINO_COMISION', 'NUMERO_RESOLUCION_COMISION', 'FECHA_INICIO_COMISION', 'FECHA_FIN_COMISION', 'OBSERVACION_COMISION'),
            'classes': ('collapse',)
        }),
        ('Condiciones', {
            'fields': ('SALARIO', 'ACTIVO', 'FECHA_INGRESO')
        }),
        ('Metadata', {
            'fields': ('FECHA_CREACION', 'FECHA_ACTUALIZACION'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('persona')
