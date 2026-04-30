from django.contrib import admin
from .models import Familiar


@admin.register(Familiar)
class FamiliarAdmin(admin.ModelAdmin):
    list_display = ('persona', 'nombre_completo', 'TIPO', 'FECHA_NACIMIENTO', 'VIVE', 'TELEFONO')
    list_filter = ('TIPO', 'VIVE')
    search_fields = ('persona__NOMBRES', 'persona__APELLIDOS', 'NOMBRE', 'APELLIDO', 'TELEFONO')
    ordering = ('persona', 'TIPO')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('persona')
