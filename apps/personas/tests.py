"""
Tests para la app personas
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from apps.usuarios.models import Usuario
from .models import Persona


class PersonaModelTestCase(TestCase):
    """Tests del modelo Persona."""

    def setUp(self):
        self.persona_data = {
            'CI_NUMERO': '1234567',
            'NOMBRES': 'Maria',
            'APELLIDOS': 'Gonzalez',
            'FECHA_NACIMIENTO': '1990-05-15',
            'ESTADO_CIVIL': 'SOLTERO',
            'TELEFONO': '0981123456',
            'EMAIL': 'maria@test.com',
        }
        self.persona = Persona.objects.create(**self.persona_data)

    def test_crear_persona(self):
        self.assertEqual(self.persona.CI_NUMERO, '1234567')
        self.assertEqual(self.persona.nombre_completo, 'Maria Gonzalez')
        self.assertTrue(self.persona.ACTIVO)

    def test_edad_calculada(self):
        # Asumiendo que hoy es 2025-03-16 y nació 1990-05-15
        # Edad = 2025 - 1990 - 1 (porque aún no cumple en mayo) = 34
        self.assertIsInstance(self.persona.edad, int)

    def test_str_representation(self):
        self.assertEqual(
            str(self.persona),
            "Maria Gonzalez - CI: 1234567"
        )


class PersonaAPITestCase(TestCase):
    """Tests de la API de personas."""

    def setUp(self):
        # Crear usuario y token
        self.user = Usuario.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123',
            CI='9876543',
            ROL='RRHH'
        )
        self.token = Token.objects.create(user=self.user)

        self.persona_data = {
            'CI_NUMERO': '1111111',
            'NOMBRES': 'Juan',
            'APELLIDOS': 'Perez',
            'FECHA_NACIMIENTO': '1995-03-20',
            'ESTADO_CIVIL': 'CASADO',
            'TELEFONO': '0981987654',
            'EMAIL': 'juan@test.com',
        }

    def test_list_personas_authenticated(self):
        """Usuario autenticado puede ver lista de personas."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(reverse('persona-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_persona(self):
        """Crear persona nueva."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(reverse('persona-list'), self.persona_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Persona.objects.count(), 1)
        self.assertEqual(Persona.objects.get().CI_NUMERO, '1111111')

    def test_ci_duplicado_no_permitido(self):
        """No permitir CI duplicados."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        # Crear primera persona
        self.client.post(reverse('persona-list'), self.persona_data, format='json')
        # Intentar crear con mismo CI
        persona_data2 = self.persona_data.copy()
        persona_data2['NOMBRES'] = 'Pedro'
        response = self.client.post(reverse('persona-list'), persona_data2, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_busqueda_por_ci(self):
        """Búsqueda por CI."""
        Persona.objects.create(**self.persona_data)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(reverse('persona-buscar-por-ci'), {'ci': '1111111'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['CI_NUMERO'], '1111111')

    def test_personas_activas(self):
        """Filtrar personas activas."""
        Persona.objects.create(**self.persona_data, ACTIVO=True)
        Persona.objects.create(
            CI_NUMERO='2222222',
            NOMBRES='Inactivo',
            APELLIDOS='Test',
            FECHA_NACIMIENTO='1980-01-01',
            ACTIVO=False
        )
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(reverse('persona-activas'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_perfil_completo(self):
        """Obtener perfil completo."""
        persona = Persona.objects.create(**self.persona_data)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(reverse('persona-perfil-completo', args=[persona.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('persona', response.data)
        self.assertIn('domicilios', response.data)
        self.assertIn('familiares', response.data)
