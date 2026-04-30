"""
Admin para DatosAcademicos
"""
from django.contrib import admin
from .models import DatosAcademicos


@admin.register(DatosAcademicos)
class DatosAcademicosAdmin(admin.ModelAdmin):
    list_display = (
        'persona',
        'NIVEL_ACADEMICO',
        'PROFESION',
        'UNIVERSIDAD',
        'ANIO_GRADUACION',
        'TIENE_POSTGRADO',
        'TIENE_MAESTRIA',
        'TIENE_DOCTORADO'
    )
    list_filter = ('NIVEL_ACADEMICO', 'TIENE_POSTGRADO', 'TIENE_MAESTRIA', 'TIENE_DOCTORADO')
    search_fields = (
        'persona__NOMBRES',
        'persona__APELLIDOS',
        'persona__CI_NUMERO',
        'PROFESION',
        'UNIVERSIDAD'
    )
    ordering = ('-FECHA_CREACION',)
    readonly_fields = ('FECHA_CREACION', 'FECHA_ACTUALIZACION')

    fieldsets = (
        ('Persona', {
            'fields': ('persona',)
        }),
        ('Formación', {
            'fields': ('NIVEL_ACADEMICO', 'PROFESION', 'UNIVERSIDAD', 'ANIO_GRADUACION')
        }),
        ('Postgrados', {
            'fields': ('TIENE_POSTGRADO', 'TIENE_MAESTRIA', 'TIENE_DOCTORADO')
        }),
        ('Metadata', {
            'fields': ('FECHA_CREACION', 'FECHA_ACTUALIZACION'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('persona')
