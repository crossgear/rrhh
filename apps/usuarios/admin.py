"""
Admin personalizado para el modelo Usuario
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.usuarios.models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """
    Admin personalizado para Usuario con campos institucionales.
    """
    list_display = (
        'username',
        'nombre_completo',
        'email',
        'CI',
        'CARGO',
        'ROL',
        'is_active',
        'is_staff',
        'date_joined'
    )
    list_filter = ('ROL', 'is_active', 'is_staff', 'date_joined')
    search_fields = (
        'username',
        'first_name',
        'last_name',
        'email',
        'CI',
        'CARGO'
    )
    ordering = ('last_name', 'first_name')

    fieldsets = UserAdmin.fieldsets + (
        ('Información Institucional', {
            'fields': ('CI', 'CARGO', 'DIRECCION_INSTITUCIONAL', 'TELEFONO_INTERNO', 'ROL')
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información Institucional', {
            'fields': ('CI', 'CARGO', 'DIRECCION_INSTITUCIONAL', 'TELEFONO_INTERNO', 'ROL')
        }),
    )

    readonly_fields = ('date_joined', 'last_login')
