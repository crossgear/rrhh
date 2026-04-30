"""
Tests para la app usuarios
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

Usuario = get_user_model()


class UsuarioModelTestCase(TestCase):
    """Tests del modelo Usuario."""

    def setUp(self):
        self.user_data = {
            'username': 'jperez',
            'first_name': 'Juan',
            'last_name': 'Perez',
            'email': 'jperez@test.com',
            'password': 'testpass123',
            'CI': '1234567',
            'CARGO': 'Analista',
            'ROL': 'RRHH'
        }
        self.usuario = Usuario.objects.create_user(**self.user_data)

    def test_crear_usuario(self):
        self.assertEqual(self.usuario.username, 'jperez')
        self.assertEqual(self.usuario.ROL, 'RRHH')
        self.assertTrue(self.usuario.is_active)

    def test_nombre_completo(self):
        self.assertEqual(self.usuario.nombre_completo, 'Juan Perez')

    def test_es_rrhh(self):
        self.assertTrue(self.usuario.es_rrhh)

    def test_es_admin(self):
        self.assertFalse(self.usuario.es_admin)


class UsuarioAPITestCase(TestCase):
    """Tests de la API de usuarios."""

    def setUp(self):
        self.admin_user = Usuario.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='adminpass',
            CI='9876543',
            CARGO='Administrador',
            ROL=Usuario.Rol.ADMIN,
            is_staff=True
        )
        self.rrhh_user = Usuario.objects.create_user(
            username='rrhh',
            email='rrhh@test.com',
            password='rrhhpass',
            CI='1111111',
            CARGO='Recursos Humanos',
            ROL=Usuario.Rol.RRHH
        )
        self.consulta_user = Usuario.objects.create_user(
            username='consultor',
            email='consultor@test.com',
            password='consultapass',
            CI='2222222',
            ROL=Usuario.Rol.CONSULTA
        )

    def test_list_usuarios_admin(self):
        """Admin puede ver todos los usuarios."""
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('usuario-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_list_usuarios_rrhh(self):
        """RRHH puede ver usuarios activos."""
        self.client.login(username='rrhh', password='rrhhpass')
        response = self.client.get(reverse('usuario-list'))
        self.assertEqual(response.status_code, 200)
        # Ve todos (admin y consulta también son activos)
        self.assertGreaterEqual(len(response.data), 2)

    def test_list_usuarios_consulta(self):
        """Consulta solo ve su propio perfil."""
        self.client.login(username='consultor', password='consultapass')
        response = self.client.get(reverse('usuario-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
