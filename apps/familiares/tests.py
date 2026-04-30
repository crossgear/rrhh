"""
Tests para la app familiares
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from apps.usuarios.models import Usuario
from apps.personas.models import Persona
from .models import Familiar


class FamiliarModelTestCase(TestCase):
    def setUp(self):
        self.persona = Persona.objects.create(
            CI_NUMERO='1234567',
            NOMBRES='Juan',
            APELLIDOS='Perez',
            FECHA_NACIMIENTO='1990-01-01'
        )
        self.familiar = Familiar.objects.create(
            persona=self.persona,
            TIPO='PADRE',
            NOMBRE='Carlos',
            APELLIDO='Perez',
            TELEFONO='0981123456'
        )

    def test_crear_familiar(self):
        self.assertEqual(self.familiar.TIPO, 'PADRE')
        self.assertTrue(self.familiar.VIVE)


class FamiliarAPITestCase(TestCase):
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
            NOMBRES='Maria',
            APELLIDOS='Gonzalez',
            FECHA_NACIMIENTO='1995-01-01'
        )

        self.familiar_data = {
            'persona': self.persona.id,
            'TIPO': 'CONYUGE',
            'NOMBRE': 'Roberto',
            'APELLIDO': 'Gonzalez',
        }

    def test_create_familiar(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(reverse('familiar-list'), self.familiar_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
