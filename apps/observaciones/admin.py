from django.contrib import admin
from .models import Observacion


@admin.register(Observacion)
class ObservacionAdmin(admin.ModelAdmin):
    list_display = ('persona', 'autor_nombre', 'FECHA', 'descripcion_corta')
    list_filter = ('FECHA',)
    search_fields = ('persona__NOMBRES', 'persona__APELLIDOS', 'DESCRIPCION')
    ordering = ('-FECHA',)
    readonly_fields = ('FECHA',)

    def descripcion_corta(self, obj):
        return obj.DESCRIPCION[:50] + '...' if len(obj.DESCRIPCION) > 50 else obj.DESCRIPCION
    descripcion_corta.short_description = 'Descripción'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('persona', 'usuario_creador')

    def has_change_permission(self, request, obj=None):
        # Las observaciones no deben editarse una vez creadas (auditoría)
        return False

    def has_delete_permission(self, request, obj=None):
        # Solo administradores pueden eliminar
        return request.user.is_authenticated and request.user.ROL == 'ADMIN'
