"""
Tests para la app observaciones
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from apps.usuarios.models import Usuario
from apps.personas.models import Persona
from .models import Observacion


class ObservacionModelTestCase(TestCase):
    def setUp(self):
        self.persona = Persona.objects.create(
            CI_NUMERO='1234567',
            NOMBRES='Juan',
            APELLIDOS='Perez',
            FECHA_NACIMIENTO='1990-01-01'
        )
        self.user = Usuario.objects.create_user(
            username='rrhh',
            password='pass',
            CI='9876543',
            ROL='RRHH'
        )
        self.observacion = Observacion.objects.create(
            persona=self.persona,
            usuario_creador=self.user,
            DESCRIPCION='Observación de prueba sobre el funcionario.'
        )

    def test_crear_observacion(self):
        self.assertEqual(self.observacion.DESCRIPCION, 'Observación de prueba sobre el funcionario.')
        self.assertEqual(self.observacion.autor_nombre, 'rrhh')


class ObservacionAPITestCase(TestCase):
    def setUp(self):
        self.user = Usuario.objects.create_user(
            username='rrhh',
            password='pass',
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

        self.observacion_data = {
            'persona': self.persona.id,
            'DESCRIPCION': 'Nueva observación importante sobre el desempeño.'
        }

    def test_create_observacion(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(reverse('observacion-list'), self.observacion_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Observacion.objects.count(), 1)

    def test_usuario_se_asigna_automaticamente(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(reverse('observacion-list'), self.observacion_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        obs = Observacion.objects.first()
        self.assertEqual(obs.usuario_creador, self.user)
