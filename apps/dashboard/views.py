"""Vistas del Dashboard"""
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.db.models import Count
from apps.personas.models import Persona
from apps.laboral.models import DatosLaborales
from apps.academico.models import DatosAcademicos
from apps.ubicacion.models import Domicilio
from apps.auditoria.models import Auditoria


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.puede_acceder_panel_rrhh:
            return redirect('mi-ficha')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_personas'] = Persona.objects.count()
        context['personas_activas'] = Persona.objects.filter(ACTIVO=True).count()
        context['personas_inactivas'] = Persona.objects.filter(ACTIVO=False).count()
        context['total_empleados'] = DatosLaborales.objects.filter(ACTIVO=True).count()
        context['por_vinculo'] = DatosLaborales.objects.filter(ACTIVO=True).values('TIPO_VINCULO').annotate(total=Count('id')).order_by('TIPO_VINCULO')
        context['por_nivel_academico'] = DatosAcademicos.objects.values('NIVEL_ACADEMICO').annotate(total=Count('id')).order_by('NIVEL_ACADEMICO')
        context['por_ciudad'] = Domicilio.objects.filter(ES_ACTUAL=True).values('CIUDAD').annotate(total=Count('id')).order_by('-total')[:10]
        context['con_postgrado'] = DatosAcademicos.objects.filter(TIENE_POSTGRADO=True).count()
        context['con_maestria'] = DatosAcademicos.objects.filter(TIENE_MAESTRIA=True).count()
        context['con_doctorado'] = DatosAcademicos.objects.filter(TIENE_DOCTORADO=True).count()
        context['top_dependencias'] = DatosLaborales.objects.filter(ACTIVO=True).values('DEPENDENCIA').annotate(total=Count('id')).order_by('-total')[:5]
        context['nombrados_total'] = DatosLaborales.objects.filter(ACTIVO=True, TIPO_VINCULO='NOMBRADO').count()
        context['contratados_total'] = DatosLaborales.objects.filter(ACTIVO=True, TIPO_VINCULO='CONTRATADO').count()
        context['pasantias_total'] = DatosLaborales.objects.filter(ACTIVO=True, TIPO_VINCULO__in=['PASANTIA','PRACTICANTE']).count()
        context['auditorias_recientes'] = Auditoria.objects.select_related('usuario')[:5]
        context['total_auditorias'] = Auditoria.objects.count()
        return context
