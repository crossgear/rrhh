"""
Tests para la app academico
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from apps.usuarios.models import Usuario
from apps.personas.models import Persona
from .models import DatosAcademicos


class DatosAcademicosModelTestCase(TestCase):
    """Tests del modelo."""

    def setUp(self):
        self.persona = Persona.objects.create(
            CI_NUMERO='1234567',
            NOMBRES='Ana',
            APELLIDOS='Martinez',
            FECHA_NACIMIENTO='1992-03-10'
        )
        self.datos = DatosAcademicos.objects.create(
            persona=self.persona,
            NIVEL_ACADEMICO='PROFESIONAL',
            PROFESION='Ingeniera Civil',
            UNIVERSIDAD='UNA',
            ANIO_GRADUACION=2015
        )

    def test_crear_datos_academicos(self):
        self.assertEqual(self.datos.NIVEL_ACADEMICO, 'PROFESIONAL')
        self.assertEqual(self.datos.PROFESION, 'Ingeniera Civil')
        self.assertEqual(self.datos.nivel_maximo, 'PROFESIONAL')

    def test_nivel_maximo_con_maestria(self):
        self.datos.TIENE_MAESTRIA = True
        self.datos.save()
        self.assertEqual(self.datos.nivel_maximo, 'MAESTRIA')


class DatosAcademicosAPITestCase(TestCase):
    """Tests de API."""

    def setUp(self):
        self.user = Usuario.objects.create_user(
            username='test',
            password='testpass',
            CI='9876543',
            ROL='RRHH'
        )
        self.token = Token.objects.create(user=self.user)

        self.persona = Persona.objects.create(
            CI_NUMERO='1111111',
            NOMBRES='Pedro',
            APELLIDOS='Lopez',
            FECHA_NACIMIENTO='1990-07-20'
        )

        self.datos_data = {
            'persona': self.persona.id,
            'NIVEL_ACADEMICO': 'MAESTRIA',
            'PROFESION': 'Máster en Administración',
            'UNIVERSIDAD': 'UC',
            'TIENE_MAESTRIA': True
        }

    def test_create_datos_academicos(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(reverse('datos_academicos-list'), self.datos_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
