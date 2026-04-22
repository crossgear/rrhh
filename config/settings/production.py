"""
Configuración para entorno de producción
"""
from .base import *


DEBUG = False

import os
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# CORS - Solo orígenes específicos
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = os.getenv(
    'CORS_ALLOWED_ORIGINS',
    'https://institucion.gov.py'
).split(',')


# Database - Usar DATABASE_URL si está disponible
import dj_database_url
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    DATABASES['default'] = dj_database_url.parse(DATABASE_URL)


# Static files - Whitenoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WHITENOISE_USE_FINDERS = True


# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True


# Logging a archivo
# LOGGING['handlers']['file']['filename'] = '/var/log/rrhh/rrhh.log'
LOGGING['root']['level'] = 'WARNING'


# Email real en producción
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'sistema@institucion.gov.py')