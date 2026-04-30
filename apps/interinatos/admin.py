from django.contrib import admin

from .models import Interinato


@admin.register(Interinato)
class InterinatoAdmin(admin.ModelAdmin):
    list_display = ('persona', 'cargo_interino', 'numero_resolucion', 'fecha_inicio', 'fecha_fin', 'estado_display')
    search_fields = ('persona__NOMBRES', 'persona__APELLIDOS', 'persona__CI_NUMERO', 'cargo_interino', 'numero_resolucion')
    list_filter = ('fecha_inicio', 'fecha_fin')
