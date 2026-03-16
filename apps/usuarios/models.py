"""
Modelo de Usuario personalizado para el sistema RRHH
Extiende AbstractUser para agregar campos institucionales
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    """
    Modelo de usuario personalizado con campos adicionales para la gestión institucional.
    """

    CI = models.CharField('Cédula', max_length=20, unique=True, blank=True, null=True)
    CARGO = models.CharField('Cargo institucional', max_length=100, blank=True)
    DIRECCION_INSTITUCIONAL = models.CharField('Dirección oficina', max_length=200, blank=True)
    TELEFONO_INTERNO = models.CharField('Tel. interno', max_length=20, blank=True)

    class Rol(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrador'
        RRHH = 'RRHH', 'Recursos Humanos'
        CONSULTA = 'CONSULTA', 'Solo Consulta'

    ROL = models.CharField(
        'Rol',
        max_length=20,
        choices=Rol.choices,
        default=Rol.CONSULTA
    )

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.get_full_name()} - {self.get_ROL_display()}"

    @property
    def nombre_completo(self):
        """Retorna el nombre completo del usuario."""
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def es_rrhh(self):
        """Verifica si el usuario tiene permisos de RRHH."""
        return self.ROL in [self.Rol.ADMIN, self.Rol.RRHH]

    @property
    def es_admin(self):
        """Verifica si el usuario es administrador."""
        return self.ROL == self.Rol.ADMIN

    def save(self, *args, **kwargs):
        """Asegurar que los superusuarios tengan rol ADMIN."""
        if self.is_superuser:
            self.ROL = self.Rol.ADMIN
        super().save(*args, **kwargs)
