# Sistema de Gestión Integral de Fichas Personales - RRHH

Sistema institucional para la gestión completa de funcionarios públicos con geoposicionamiento, desarrollado con Django, Django REST Framework y PostgreSQL+PostGIS.

## Características

- Gestión completa de personas y datos personales
- Registro de domicilios con geoposicionamiento (PointField PostGIS)
- Datos laborales con tipos de vínculo
- Historial académico y postgrados
- Registro de familiares
- Sistema de observaciones con auditoría
- Dashboard con estadísticas en tiempo real
- API REST completa con autenticación
- Mapas interactivos con Leaflet
- Control de permisos por roles (ADMIN, RRHH, CONSULTA)
- Dockerizado y listo para producción

## Stack Tecnológico

- **Backend**: Django 5.x LTS + Django REST Framework
- **Base de datos**: PostgreSQL 15 + PostGIS
- **GIS**: Django GIS (PointField SRID 4326)
- **Frontend**: Bootstrap 5, Leaflet JS
- **Autenticación**: Token + Session + JWT opcional
- **Contenedores**: Docker + Docker Compose

## Requisitos del Sistema

### Desarrollo Local (sin Docker)

- Python 3.11 o superior
- PostgreSQL 12+ con PostGIS
- pip

### Desarrollo con Docker

- Docker y Docker Compose

## Instalación Rápida

### Opción 1: Con Docker (Recomendado)

```bash
# 1. Clonar proyecto
cd RRHH

# 2. Copiar variables de entorno
cp .env.example .env
# Editar .env si es necesario

# 3. Inicializar sistema
chmod +x scripts/init.sh
./scripts/init.sh

# 4. Acceder a:
# - Dashboard: http://localhost:8000/dashboard/
# - Login: http://localhost:8000/accounts/login/
# - Admin: http://localhost:8000/admin/
# - API: http://localhost:8000/api/
```

### Opción 2: Desarrollo Manual

```bash
# 1. Crear entorno virtual
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 2. Instalar dependencias
pip install -r requirements/development.txt

# 3. Configurar variables de entorno
cp .env.example .env
# Editar .env con datos de tu PostgreSQL local

# 4. Configurar base de datos PostgreSQL
# Crear base de datos y extensión PostGIS:
# CREATE DATABASE rrhh_db;
# \c rrhh_db
# CREATE EXTENSION postgis;

# 5. Ejecutar migraciones
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# 6. Servidor de desarrollo
python manage.py runserver

# 7. Acceder a http://localhost:8000/dashboard/
```

## Configuración Inicial

1. **Superusuario**: Se crea automáticamente `admin / admin123` (cambiar en producción)
2. **Roles de usuario**:
   - `ADMIN`: Acceso total
   - `RRHH`: Puede editar personas, datos laborales, académicos, crear observaciones
   - `CONSULTA`: Solo lectura (ver listados y detalles)

3. **Extensión PostGIS**: Requerida en PostgreSQL
```sql
CREATE EXTENSION IF NOT EXISTS postgis;
```

## Estructura del Proyecto

```
RRHH/
├── apps/
│   ├── usuarios/       # Gestión de usuarios (Custom User)
│   ├── personas/       # Modelo principal Persona
│   ├── ubicacion/      # Domicilios con PointField (GIS)
│   ├── laboral/        # Datos laborales
│   ├── academico/      # Datos académicos
│   ├── familiares/     # Familiares del funcionario
│   ├── observaciones/  # Observaciones/notas
│   └── dashboard/      # Dashboard principal
├── config/             # Configuración del proyecto Django
│   └── settings/       # Configuraciones por entorno
├── templates/          # Templates HTML
├── static/             # CSS, JS, imágenes
├── requirements/       # Dependencias Python
├── scripts/            # Scripts de inicialización
└── docker-compose.yml
```

## API REST Endpoints

### Autenticación
- `POST /api/token/` - Obtener token
- `POST /api/auth/login/` - Login session

### Personas
- `GET /api/personas/` - Listar personas (filtrado por búsqueda)
- `POST /api/personas/` - Crear persona (RRHH/Admin)
- `GET /api/personas/{id}/` - Detalle persona
- `PUT/PATCH /api/personas/{id}/` - Actualizar persona (RRHH/Admin)
- `GET /api/personas/{id}/perfil_completo/` - Perfil completo con relaciones

### Domicilios
- `GET /api/ubicacion/domicilios/` - Listar domicilios
- `POST /api/ubicacion/domicilios/` - Crear domicilio (con lat/long)
- `GET /api/ubicacion/mapa/?format=geojson` - GeoJSON para mapa
- `GET /api/ubicacion/domicilios/por_persona/?persona_id=X` - Domicilios de persona

### Usuarios
- `GET /api/usuarios/` - Listar usuarios (filtrado por rol)
- `POST /api/usuarios/` - Crear usuario (Admin)
- `GET /api/usuarios/perfil/` - Perfil del usuario actual

### Datos Laborales, Académicos, Familiares, Observaciones
- Endpoints CRUD estándar bajo `/api/{recurso}/`

## GIS y Mapas

### Modelo Domicilio (PointField)

```python
class Domicilio(models.Model):
    persona = models.ForeignKey(Persona, ...)
    LATITUD = models.DecimalField(...)
    LONGITUD = models.DecimalField(...)
    UBICACION = gis.PointField(srid=4326)  # Se crea automáticamente
```

### Endpoint GeoJSON

```
GET /api/ubicacion/mapa/?format=geojson
```

Devuelve:
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {"type": "Point", "coordinates": [-58.3833, -25.2637]},
      "properties": {
        "persona_nombre": "Juan Perez",
        "persona_ci": "1234567",
        "DIRECCION": "Calle Test 123",
        "CIUDAD": "Asunción"
      }
    }
  ]
}
```

### Consumir GeoJSON en Frontend (Leaflet)

```javascript
fetch('/api/ubicacion/mapa/?format=geojson')
    .then(response => response.json())
    .then(data => {
        L.geoJSON(data, {
            pointToLayer: function(feature, latlng) {
                return L.marker(latlng);
            },
            onEachFeature: function(feature, layer) {
                layer.bindPopup(feature.properties.popup_html);
            }
        }).addTo(map);
    });
```

## Dashboard

El dashboard muestra estadísticas en tiempo real:

- Total de personas registradas
- Personas activas/inactivas
- Funcionarios por tipo de vínculo (gráfico torta)
- Funcionarios por nivel académico (gráfico barra)
- Top 10 ciudades con más funcionarios
- Top 5 dependencias
- Conteo de postgrados, maestrías, doctorados

## Permisos y Seguridad

### Niveles de acceso

| Rol | Ver personas | Editar personas | Crear/Modificar datos laborales | Ver observaciones | Admin site |
|-----|--------------|------------------|----------------------------------|-------------------|------------|
| ADMIN | ✅ | ✅ | ✅ | ✅ | ✅ |
| RRHH | ✅ | ✅ | ✅ | ✅ | ❌ |
| CONSULTA | ✅ | ❌ | ❌ | ❌ | ❌ |

### Implementación

```python
# permisos.py
class IsRRHHOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.ROL in ['ADMIN', 'RRHH']

# views
permission_classes = [IsRRHHOrAdmin]
```

## Despliegue en Producción

### Variables de entorno de producción

```bash
DEBUG=False
SECRET_KEY=tu-clave-secreta-muy-larga-y-segura
ALLOWED_HOSTS=tu-dominio.gov.py,www.tu-dominio.gov.py
DB_NAME=rrhh_db
DB_USER=postgres
DB_PASSWORD=contraseña-segura
DB_HOST=db-host
CORS_ALLOWED_ORIGINS=https://frontend.tu-dominio.gov.py
```

### Usar docker-compose.prod.yml

```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Configuraciones adicionales

- HTTPS activado (SECURE_SSL_REDIRECT)
- Headers de seguridad (HSTS, CSP)
- Whitenoise para archivos estáticos
- Logging a archivos
- Backup automático de PostgreSQL

## Desarrollo

### Crear migraciones

```bash
python manage.py makemigrations <app>
python manage.py migrate
```

### Crear superusuario

```bash
python manage.py createsuperuser
# Username: admin
# Email: admin@institucion.gov.py
```

### Pruebas

```bash
# Ejecutar tests
python manage.py test

# Tests específicos
python manage.py test apps.personas
```

### Verificar conexión a PostGIS

```bash
python manage.py shell
>>> from django.contrib.gis.geos import Point
>>> p = Point(-58.3833, -25.2637)
>>> print(p)
```

## Solución de Problemas

### Error: "Could not find the GDAL library"

- **Windows**: Instalar OSGeo4W y configurar `GDAL_LIBRARY_PATH`
- **Linux**: `apt-get install gdal-bin libgdal-dev`
- **Docker**: Ya configurado en Dockerfile

### Error: "Extension postgis does not exist"

```sql
-- En PostgreSQL
CREATE EXTENSION postgis;
```

### Error al hacer migrate

```bash
# Verificar conexión a DB
python manage.py check
# Ver variables de entorno
python -c "import os; print(os.getenv('DB_HOST'))"
```

## Contribuciones

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abrir Pull Request

## Licencia

Propiedad de la Institución. Todos los derechos reservados.

## Soporte

Para soporte técnico, contactar al equipo de desarrollo:
- Email: sistemas@institucion.gov.py
- Teléfono: (595) 21 123 456
