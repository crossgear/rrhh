from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Auditoria


class AuditoriaListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Auditoria
    template_name = 'auditoria/list.html'
    context_object_name = 'auditorias'
    paginate_by = 25

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.puede_acceder_panel_rrhh

    def get_queryset(self):
        qs = super().get_queryset().select_related('usuario')
        usuario = self.request.GET.get('usuario', '').strip()
        accion = self.request.GET.get('accion', '').strip()
        texto = self.request.GET.get('search', '').strip()

        if usuario:
            qs = qs.filter(usuario__username__iexact=usuario)
        if accion:
            qs = qs.filter(accion=accion)
        if texto:
            qs = qs.filter(descripcion__icontains=texto)
        return qs
