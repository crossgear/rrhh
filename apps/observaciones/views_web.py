"""
Vistas web para observaciones
"""
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse

from apps.personas.models import Persona
from .models import Observacion


class ObservacionCreateView(LoginRequiredMixin, CreateView):
    """
    Vista para crear observación desde el perfil de persona.
    """
    model = Observacion
    fields = ['DESCRIPCION']
    template_name = 'observaciones/form.html'

    def dispatch(self, request, *args, **kwargs):
        # Verificar que el usuario tenga permiso
        if not request.user.es_rrhh:
            messages.error(request, 'No tiene permisos para crear observaciones.')
            return redirect('persona-list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        persona_id = self.request.POST.get('persona')
        persona = get_object_or_404(Persona, id=persona_id)

        observacion = form.save(commit=False)
        observacion.persona = persona
        observacion.usuario_creador = self.request.user
        observacion.save()

        messages.success(self.request, 'Observación agregada exitosamente.')
        return redirect('persona-detail', pk=persona.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        persona_id = self.request.GET.get('persona') or self.request.POST.get('persona')
        if persona_id:
            context['persona'] = get_object_or_404(Persona, id=persona_id)
        return context

    def get_initial(self):
        initial = super().get_initial()
        persona_id = self.request.GET.get('persona')
        if persona_id:
            initial['persona'] = persona_id
        return initial
