from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView

from apps.auditoria.utils import registrar_auditoria
from apps.personas.models import Persona
from apps.personas.views_web import RRHHRequiredMixin

from .forms import InterinatoForm
from .models import Interinato


def interinato_snapshot(interinato):
    if not interinato:
        return {}
    return {
        'funcionario': interinato.persona.nombre_completo,
        'cargo_interino': interinato.cargo_interino,
        'dependencia': interinato.dependencia,
        'numero_resolucion': interinato.numero_resolucion,
        'fecha_resolucion': interinato.fecha_resolucion.isoformat() if interinato.fecha_resolucion else '',
        'fecha_inicio': interinato.fecha_inicio.isoformat() if interinato.fecha_inicio else '',
        'fecha_fin': interinato.fecha_fin.isoformat() if interinato.fecha_fin else '',
        'archivo_resolucion': interinato.archivo_resolucion.name if interinato.archivo_resolucion else '',
        'observacion': interinato.observacion,
        'estado': interinato.estado_display,
    }


class InterinatoFormMixin(RRHHRequiredMixin):
    model = Interinato
    form_class = InterinatoForm
    template_name = 'interinatos/form.html'

    def get_success_url(self):
        return reverse('persona-detail', kwargs={'pk': self.object.persona_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['persona'] = getattr(self, 'persona', None) or getattr(self.object, 'persona', None)
        context['titulo'] = getattr(self, 'titulo', 'Interinato')
        return context


class InterinatoCreateView(InterinatoFormMixin, CreateView):
    titulo = 'Registrar interinato'

    def dispatch(self, request, *args, **kwargs):
        self.persona = get_object_or_404(Persona, pk=kwargs['persona_pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.persona = self.persona
        form.instance.creado_por = self.request.user
        response = super().form_valid(form)
        registrar_auditoria(
            usuario=self.request.user,
            accion='CREAR',
            modelo='Interinato',
            objeto_id=self.object.pk,
            objeto_repr=f'{self.object.persona.nombre_completo} - {self.object.cargo_interino}',
            descripcion=f'Registró interinato de {self.object.persona.nombre_completo} como {self.object.cargo_interino}.',
            despues=interinato_snapshot(self.object),
        )
        messages.success(self.request, 'Interinato registrado correctamente.')
        return response


class InterinatoUpdateView(InterinatoFormMixin, UpdateView):
    titulo = 'Editar interinato'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.persona = self.object.persona
        return self.object

    def form_valid(self, form):
        datos_antes = interinato_snapshot(self.get_object())
        response = super().form_valid(form)
        registrar_auditoria(
            usuario=self.request.user,
            accion='EDITAR',
            modelo='Interinato',
            objeto_id=self.object.pk,
            objeto_repr=f'{self.object.persona.nombre_completo} - {self.object.cargo_interino}',
            descripcion=f'Editó interinato de {self.object.persona.nombre_completo}.',
            antes=datos_antes,
            despues=interinato_snapshot(self.object),
        )
        messages.success(self.request, 'Interinato actualizado correctamente.')
        return response


class InterinatoDeleteView(RRHHRequiredMixin, DeleteView):
    model = Interinato
    template_name = 'interinatos/confirm_delete.html'

    def get_success_url(self):
        return reverse('persona-detail', kwargs={'pk': self.object.persona_id})

    def form_valid(self, form):
        datos_antes = interinato_snapshot(self.object)
        registrar_auditoria(
            usuario=self.request.user,
            accion='ELIMINAR',
            modelo='Interinato',
            objeto_id=self.object.pk,
            objeto_repr=f'{self.object.persona.nombre_completo} - {self.object.cargo_interino}',
            descripcion=f'Eliminó interinato de {self.object.persona.nombre_completo}.',
            antes=datos_antes,
        )
        messages.success(self.request, 'Interinato eliminado correctamente.')
        return super().form_valid(form)
