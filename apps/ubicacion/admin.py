"""
Admin para Domicilio con mapa integrado (OSMGeoAdmin)
"""
from django.contrib import admin
from apps.personas.models import Persona
from .models import Domicilio


@admin.register(Domicilio)
class DomicilioAdmin(admin.ModelAdmin):
    """
    Admin con mapa OpenStreetMap integrado para edición de puntos.
    """
    list_display = (
        'persona',
        'DIRECCION',
        'BARRIO',
        'CIUDAD',
        'ES_ACTUAL',
        'LATITUD',
        'LONGITUD',
        'FECHA_REGISTRO'
    )
    list_filter = ('CIUDAD', 'ES_ACTUAL')
    search_fields = (
        'persona__NOMBRES',
        'persona__APELLIDOS',
        'persona__CI_NUMERO',
        'DIRECCION',
        'BARRIO',
        'CIUDAD'
    )
    ordering = ('-FECHA_REGISTRO',)

    # Configuración del mapa en admin
    default_lon = -58.3833  # Asunción, Paraguay
    default_lat = -25.2637
    default_zoom = 10

    # Campos mostrados en el formulario de mapa
    map_template = 'gis/admin/openlayers.html'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('persona')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "persona":
            kwargs["queryset"] = Persona.objects.all().order_by('APELLIDOS', 'NOMBRES')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
