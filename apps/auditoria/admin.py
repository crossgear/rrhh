from django.contrib import admin
from .models import Auditoria


@admin.register(Auditoria)
class AuditoriaAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'usuario', 'accion', 'modelo', 'objeto_repr')
    list_filter = ('accion', 'modelo', 'fecha')
    search_fields = ('objeto_repr', 'descripcion', 'usuario__username')
    readonly_fields = ('fecha', 'usuario', 'accion', 'modelo', 'objeto_id', 'objeto_repr', 'descripcion', 'datos_antes', 'datos_despues')
