"""
Admin para el modelo Persona
"""
from django.contrib import admin
from .models import Persona


@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    """
    Admin optimizado para gestión de personas.
    """
    list_display = (
        'CI_NUMERO',
        'nombre_completo',
        'FECHA_NACIMIENTO',
        'edad',
        'ESTADO_CIVIL',
        'TELEFONO',
        'EMAIL',
        'ACTIVO',
        'tiene_datos_laborales',
        'tiene_datos_academicos',
    )
    list_filter = ('ESTADO_CIVIL', 'ACTIVO', 'FECHA_CREACION')
    search_fields = ('CI_NUMERO', 'NOMBRES', 'APELLIDOS', 'TELEFONO', 'EMAIL')
    ordering = ('APELLIDOS', 'NOMBRES')
    readonly_fields = ('FECHA_CREACION', 'FECHA_ACTUALIZACION')

    fieldsets = (
        ('Datos Personales', {
            'fields': ('CI_NUMERO', ('NOMBRES', 'APELLIDOS'), 'FECHA_NACIMIENTO', 'ESTADO_CIVIL')
        }),
        ('Contacto', {
            'fields': ('TELEFONO', 'EMAIL')
        }),
        ('Estado', {
            'fields': ('ACTIVO',)
        }),
        ('Metadata', {
            'fields': ('FECHA_CREACION', 'FECHA_ACTUALIZACION'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related()
