"""URL configuration for config project."""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from django.views.generic import RedirectView
from rest_framework.authtoken import views as drf_authtoken

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='dashboard-index', permanent=False)),
    # Admin
    path('admin/', admin.site.urls),

    # Autenticación web
    path('accounts/', include('apps.usuarios.urls_web')),

    # API REST
    path('api/auth/', include('rest_framework.urls')),
    path('api/token/', drf_authtoken.obtain_auth_token),
    path('api/usuarios/', include('apps.usuarios.urls')),
    path('api/personas/', include('apps.personas.urls')),
    path('api/ubicacion/', include('apps.ubicacion.urls')),
    path('api/laboral/', include('apps.laboral.urls')),
    path('api/academico/', include('apps.academico.urls')),
    path('api/familiares/', include('apps.familiares.urls')),
    path('api/observaciones/', include('apps.observaciones.urls')),
    path('observaciones/', include('apps.observaciones.urls')),

    # Vistas web
    path('personas/', include('apps.personas.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('auditoria/', include('apps.auditoria.urls')),
    path('interinatos/', include('apps.interinatos.urls')),
]

# Vistas personalizadas de error
handler400 = 'config.views.bad_request'
handler403 = 'config.views.permission_denied'
handler404 = 'config.views.page_not_found'
handler500 = 'config.views.server_error'

# Servir archivos media/static en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)