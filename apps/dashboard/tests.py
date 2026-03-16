"""
Tests para Dashboard
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.usuarios.models import Usuario
from apps.personas.models import Persona


class DashboardViewTestCase(TestCase):
    """Tests de la vista Dashboard."""

    def setUp(self):
        self.user = Usuario.objects.create_user(
            username='testuser',
            password='testpass',
            CI='9876543',
            ROL='RRHH'
        )

    def test_dashboard_requires_login(self):
        """Dashboard requiere autenticación."""
        response = self.client.get(reverse('dashboard-index'))
        self.assertEqual(response.status_code, 302)  # Redirect a login
        self.assertIn('/login/', response.url)

    def test_dashboard_loads_for_authenticated_user(self):
        """Dashboard carga para usuario autenticado."""
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('dashboard-index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/index.html')

    def test_dashboard_context_stats(self):
        """Dashboard incluye estadísticas en contexto."""
        # Crear datos de prueba
        Persona.objects.create(
            CI_NUMERO='1111111',
            NOMBRES='Test',
            APELLIDOS='User',
            FECHA_NACIMIENTO='1990-01-01'
        )
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('dashboard-index'))
        self.assertIn('total_personas', response.context)
        self.assertEqual(response.context['total_personas'], 1)
