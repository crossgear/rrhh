"""
Tests para la app ubicacion (GIS)
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from apps.usuarios.models import Usuario
from apps.personas.models import Persona
from .models import Domicilio


class DomicilioModelTestCase(TestCase):
    """Tests del modelo Domicilio."""

    def setUp(self):
        self.persona = Persona.objects.create(
            CI_NUMERO='1234567',
            NOMBRES='Juan',
            APELLIDOS='Perez',
            FECHA_NACIMIENTO='1990-01-01'
        )
        self.domicilio_data = {
            'persona': self.persona,
            'DIRECCION': 'Calle Test 123',
            'BARRIO': 'Centro',
            'CIUDAD': 'Asunción',
            'LATITUD': -25.2637,
            'LONGITUD': -58.3833,
            'ES_ACTUAL': True
        }
        self.domicilio = Domicilio.objects.create(**self.domicilio_data)

    def test_crear_domicilio(self):
        self.assertEqual(self.domicilio.DIRECCION, 'Calle Test 123')
        self.assertEqual(self.domicilio.CIUDAD, 'Asunción')
        self.assertTrue(self.domicilio.ES_ACTUAL)
        self.assertIsNotNone(self.domicilio.UBICACION)

    def test_pointfield_creado(self):
        """Verificar que PointField se crea correctamente."""
        self.assertIsNotNone(self.domicilio.UBICACION)
        self.assertEqual(self.domicilio.UBICACION.geom_type, 'Point')

    def test_coordenadas_dict(self):
        coords = self.domicilio.coordenadas_dict
        self.assertIsNotNone(coords)
        self.assertEqual(coords['lat'], -25.2637)
        self.assertEqual(coords['lng'], -58.3833)

    def test_save_crea_point_desde_latlon(self):
        """Al guardar con lat/long, se crea PointField automáticamente."""
        domicilio = Domicilio(
            persona=self.persona,
            DIRECCION='Otra calle',
            CIUDAD='Encarnación',
            LATITUD=-27.3333,
            LONGITUD=-55.8667
        )
        domicilio.save()
        self.assertIsNotNone(domicilio.UBICACION)

    def test_desactivar_anteriores(self):
        """Al crear un domicilio actual, otros anteriores se desactivan."""
        # Crear primer domicilio actual
        d1 = Domicilio.objects.create(
            persona=self.persona,
            DIRECCION='Calle Antigua 1',
            CIUDAD='Asunción',
            LATITUD=-25.1,
            LONGITUD=-58.1,
            ES_ACTUAL=True
        )
        # Crear segundo domicilio actual
        d2 = Domicilio.objects.create(
            persona=self.persona,
            DIRECCION='Calle Nueva 1',
            CIUDAD='Asunción',
            LATITUD=-25.2,
            LONGITUD=-58.2,
            ES_ACTUAL=True
        )
        # Verificar que solo d2 es actual
        d1.refresh_from_db()
        d2.refresh_from_db()
        self.assertFalse(d1.ES_ACTUAL)
        self.assertTrue(d2.ES_ACTUAL)


class DomicilioAPITestCase(TestCase):
    """Tests de la API de domicilios."""

    def setUp(self):
        self.user = Usuario.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass',
            CI='9876543'
        )
        self.token = Token.objects.create(user=self.user)

        self.persona = Persona.objects.create(
            CI_NUMERO='1111111',
            NOMBRES='Maria',
            APELLIDOS='Gonzalez',
            FECHA_NACIMIENTO='1995-01-01'
        )

        self.domicilio_data = {
            'persona': self.persona.id,
            'DIRECCION': 'Av. Principal 456',
            'BARRIO': 'Villa Morra',
            'CIUDAD': 'Asunción',
            'LATITUD': -25.3,
            'LONGITUD': -58.4,
            'ES_ACTUAL': True
        }

    def test_create_domicilio(self):
        """Crear domicilio con lat/long."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(
            reverse('domicilio-list'),
            self.domicilio_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Domicilio.objects.count(), 1)
        domicilio = Domicilio.objects.first()
        self.assertIsNotNone(domicilio.UBICACION)

    def test_geojson_endpoint(self):
        """Endpoint GeoJSON devuelve formato correcto."""
        Domicilio.objects.create(
            persona=self.persona,
            DIRECCION='Test 123',
            CIUDAD='Asunción',
            LATITUD=-25.26,
            LONGITUD=-58.38,
            ES_ACTUAL=True
        )
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(reverse('mapa-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('features', response.data)
        self.assertEqual(response.data['type'], 'FeatureCollection')

    def test_geo_feature_structure(self):
        """Verificar estructura GeoJSON."""
        Domicilio.objects.create(
            persona=self.persona,
            DIRECCION='Geo Test',
            CIUDAD='Ciudad del Este',
            LATITUD=-25.5,
            LONGITUD=-54.6,
            ES_ACTUAL=True
        )
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(reverse('mapa-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        feature = response.data['features'][0]
        self.assertIn('type', feature)
        self.assertIn('geometry', feature)
        self.assertIn('properties', feature)
        self.assertEqual(feature['type'], 'Feature')
        self.assertEqual(feature['geometry']['type'], 'Point')
