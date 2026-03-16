"""
Vistas del Dashboard
"""
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from apps.personas.models import Persona
from apps.laboral.models import DatosLaborales
from apps.academico.models import DatosAcademicos
from apps.ubicacion.models import Domicilio


class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Dashboard principal con estadísticas del sistema.
    """
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Estadísticas generales
        context['total_personas'] = Persona.objects.count()
        context['personas_activas'] = Persona.objects.filter(ACTIVO=True).count()
        context['personas_inactivas'] = Persona.objects.filter(ACTIVO=False).count()

        # Estadísticas laborales
        context['total_empleados'] = DatosLaborales.objects.filter(ACTIVO=True).count()

        # Por tipo de vínculo
        context['por_vinculo'] = DatosLaborales.objects.filter(ACTIVO=True).values(
            'TIPO_VINCULO'
        ).annotate(total=Count('id')).order_by('TIPO_VINCULO')

        # Por nivel académico
        context['por_nivel_academico'] = DatosAcademicos.objects.values(
            'NIVEL_ACADEMICO'
        ).annotate(total=Count('id')).order_by('NIVEL_ACADEMICO')

        # Por ciudad (domicilios actuales)
        context['por_ciudad'] = Domicilio.objects.filter(ES_ACTUAL=True).values(
            'CIUDAD'
        ).annotate(total=Count('id')).order_by('-total')[:10]

        # Funcionarios con postgrados
        context['con_postgrado'] = DatosAcademicos.objects.filter(TIENE_POSTGRADO=True).count()
        context['con_maestria'] = DatosAcademicos.objects.filter(TIENE_MAESTRIA=True).count()
        context['con_doctorado'] = DatosAcademicos.objects.filter(TIENE_DOCTORADO=True).count()

        # Top dependencias con más personal
        context['top_dependencias'] = DatosLaborales.objects.filter(ACTIVO=True).values(
            'DEPENDENCIA'
        ).annotate(total=Count('id')).order_by('-total')[:5]

        return context
