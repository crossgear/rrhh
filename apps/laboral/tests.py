"""
Tests para la app laboral
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from apps.usuarios.models import Usuario
from apps.personas.models import Persona
from .models import DatosLaborales


class DatosLaboralesModelTestCase(TestCase):
    """Tests del modelo DatosLaborales."""

    def setUp(self):
        self.persona = Persona.objects.create(
            CI_NUMERO='1234567',
            NOMBRES='Juan',
            APELLIDOS='Perez',
            FECHA_NACIMIENTO='1990-01-01'
        )
        self.datos_laborales = DatosLaborales.objects.create(
            persona=self.persona,
            TIPO_VINCULO='PLANTA',
            INSTITUCION='Municipalidad',
            DEPENDENCIA='Dirección de Informática',
            CARGO='Analista de Sistemas',
            SALARIO=5000000,
            FECHA_INGRESO='2020-01-15'
        )

    def test_crear_datos_laborales(self):
        self.assertEqual(self.datos_laborales.TIPO_VINCULO, 'PLANTA')
        self.assertEqual(self.datos_laborales.CARGO, 'Analista de Sistemas')
        self.assertEqual(self.datos_laborales.SALARIO, 5000000)
        self.assertTrue(self.datos_laborales.ACTIVO)


class DatosLaboralesAPITestCase(TestCase):
    """Tests de la API."""

    def setUp(self):
        self.user = Usuario.objects.create_user(
            username='testuser',
            password='testpass',
            CI='9876543',
            ROL='RRHH'
        )
        self.token = Token.objects.create(user=self.user)

        self.persona = Persona.objects.create(
            CI_NUMERO='1111111',
            NOMBRES='Maria',
            APELLIDOS='Gonzalez',
            FECHA_NACIMIENTO='1995-01-01'
        )

        self.datos_data = {
            'persona': self.persona.id,
            'TIPO_VINCULO': 'CONTRATADO',
            'INSTITUCION': 'Municipalidad',
            'DEPENDENCIA': 'Recursos Humanos',
            'CARGO': 'Asistente',
            'SALARIO': 3000000,
            'FECHA_INGRESO': '2022-06-01'
        }

    def test_create_datos_laborales(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(reverse('datos_laborales-list'), self.datos_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DatosLaborales.objects.count(), 1)
