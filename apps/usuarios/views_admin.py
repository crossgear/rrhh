from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView

from .models_admin import UsuarioAdministradorRRHH


class SoloAdminRRHHMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.es_admin_rrhh


class AdminRRHHListView(SoloAdminRRHHMixin, ListView):
    model = UsuarioAdministradorRRHH
    template_name = "usuarios/admin_list.html"
    context_object_name = "admins"

    def get_queryset(self):
        return UsuarioAdministradorRRHH.objects.filter(activo=True).order_by("username")


class AdminRRHHCreateView(SoloAdminRRHHMixin, CreateView):
    model = UsuarioAdministradorRRHH
    fields = ["username"]
    template_name = "usuarios/admin_form.html"
    success_url = reverse_lazy("admin-rrhh-list")

    def form_valid(self, form):
        form.instance.username = form.instance.username.strip().lower()
        form.instance.creado_por = self.request.user
        return super().form_valid(form)


class AdminRRHHDeleteView(SoloAdminRRHHMixin, DeleteView):
    model = UsuarioAdministradorRRHH
    template_name = "usuarios/admin_confirm_delete.html"
    success_url = reverse_lazy("admin-rrhh-list")

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.username == request.user.username_normalized:
            return redirect("admin-rrhh-list")
        return super().dispatch(request, *args, **kwargs)
