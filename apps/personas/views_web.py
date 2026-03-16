"""
Vistas web (CBV) para frontend de Personas
"""
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q

from .models import Persona
from .forms import PersonaForm


class PersonaListView(LoginRequiredMixin, ListView):
    """
    Vista de lista de personas con búsqueda y filtros.
    """
    model = Persona
    template_name = 'personas/list.html'
    context_object_name = 'object_list'
    paginate_by = 20

    def get_queryset(self):
        queryset = Persona.objects.all()

        # Búsqueda por texto
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(CI_NUMERO__icontains=search) |
                Q(NOMBRES__icontains=search) |
                Q(APELLIDOS__icontains=search) |
                Q(TELEFONO__icontains=search) |
                Q(EMAIL__icontains=search)
            )

        # Filtro por estado civil
        estado_civil = self.request.GET.get('ESTADO_CIVIL')
        if estado_civil:
            queryset = queryset.filter(ESTADO_CIVIL=estado_civil)

        # Filtro por activo
        activo = self.request.GET.get('ACTIVO')
        if activo == 'true':
            queryset = queryset.filter(ACTIVO=True)
        elif activo == 'false':
            queryset = queryset.filter(ACTIVO=False)

        return queryset.order_by('APELLIDOS', 'NOMBRES')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estado_civil_choices'] = Persona.ESTADO_CIVIL_CHOICES
        return context


class PersonaDetailView(LoginRequiredMixin, DetailView):
    """
    Vista de detalle de persona.
    """
    model = Persona
    template_name = 'personas/detail.html'
    context_object_name = 'persona'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        persona = self.object

        # Obtener datos relacionados
        try:
            context['datos_laborales'] = persona.datos_laborales
        except:
            context['datos_laborales'] = None

        try:
            context['datos_academicos'] = persona.datos_academicos
        except:
            context['datos_academicos'] = None

        # Domicilios (ya están en persona.domicilios.all)
        # Familiares
        context['familiares'] = persona.familiares.all()

        # Observaciones
        context['observaciones'] = persona.observaciones.all()[:10]

        return context


class PersonaCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Vista para crear nueva persona. Solo RRHH.
    """
    model = Persona
    template_name = 'personas/form.html'
    form_class = PersonaForm
    success_url = reverse_lazy('persona-list')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.es_rrhh

    def form_valid(self, form):
        messages.success(self.request, 'Persona creada exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error al crear persona. Verifique los datos.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nueva Persona'
        context['estado_civil_choices'] = Persona.ESTADO_CIVIL_CHOICES
        return context


class PersonaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Vista para editar persona. Solo RRHH.
    """
    model = Persona
    template_name = 'personas/form.html'
    form_class = PersonaForm
    success_url = reverse_lazy('persona-list')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.es_rrhh

    def form_valid(self, form):
        messages.success(self.request, 'Persona actualizada exitosamente.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Persona'
        context['estado_civil_choices'] = Persona.ESTADO_CIVIL_CHOICES
        return context


class PersonaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Vista para eliminar persona. Solo Admin.
    """
    model = Persona
    template_name = 'personas/confirm_delete.html'
    success_url = reverse_lazy('persona-list')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.es_admin

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Persona eliminada exitosamente.')
        return super().delete(request, *args, **kwargs)


class MapaPersonasView(LoginRequiredMixin, TemplateView):
    """
    Vista del mapa de funcionarios.
    """
    template_name = 'personas/mapa.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener lista de ciudades para filtro
        from apps.ubicacion.models import Domicilio
        ciudades = Domicilio.objects.values('CIUDAD').distinct().order_by('CIUDAD')
        context['ciudades'] = ciudades

        return context
