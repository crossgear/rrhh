from django.conf import settings
from django.db import models


class UsuarioAdministradorRRHH(models.Model):
    username = models.CharField(max_length=150, unique=True)
    activo = models.BooleanField(default=True)
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="admins_rrhh_creados",
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Administrador RRHH"
        verbose_name_plural = "Administradores RRHH"
        ordering = ["username"]

    def save(self, *args, **kwargs):
        if self.username:
            self.username = self.username.strip().lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
