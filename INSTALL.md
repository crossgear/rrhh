# Guía de Instalación Paso a Paso

## Sistema de Gestión Integral de Fichas Personales - RRHH

Esta guía cubre la instalación completa del sistema en diferentes entornos.

---

## Tabla de Contenidos

1. [Requisitos previos](#requisitos-previos)
2. [Instalación con Docker (Recomendado)](#instalación-con-docker)
3. [Instalación Manual](#instalación-manual)
4. [Configuración Post-Instalación](#configuración-post-instalación)
5. [Solución de problemas](#solución-de-problemas)

---

## Requisitos Previos

### Para Docker (Recomendado)
- Docker 20.10+
- Docker Compose 2.0+
- 4GB RAM mínima
- 10GB espacio en disco

### Para Instalación Manual
- Python 3.11 o 3.12
- PostgreSQL 12+ con PostGIS
- pip
- Virtualenv (recomendado)

---

## Instalación con Docker

### Paso 1: Obtener el código

```bash
git clone <repositorio>
cd RRHH
```

### Paso 2: Variables de entorno

```bash
cp .env.example .env
```

Editar `.env` si es necesario. Valores por defecto funcionan para desarrollo.

### Paso 3: Inicializar sistema

```bash
chmod +x scripts/init.sh
./scripts/init.sh
```

Este script automáticamente:
- Instala dependencias Python
- Configura variables de entorno
- Inicia PostgreSQL con PostGIS
- Aplica migraciones
- Crea superusuario admin/admin123
- Recolecta archivos estáticos

### Paso 4: Acceder al sistema

```bash
# Dashboard
http://localhost:8000/dashboard/

# Login
http://localhost:8000/accounts/login/
Username: admin
Password: admin123

# Admin Django
http://localhost:8000/admin/

# API REST
http://localhost:8000/api/personas/
```

### Paso 5: Detener servicios

```bash
docker-compose down
# Para eliminar datos también:
docker-compose down -v
```

---

## Instalación Manual

### Paso 1: Instalar dependencias del sistema

#### Ubuntu/Debian

```bash
sudo apt-get update
sudo apt-get install -y python3.11 python3.11-venv python3-pip postgresql postgresql-contrib postgis gdal-bin libgdal-dev
```

#### Windows

1. Instalar Python 3.11 desde python.org
2. Instalar PostgreSQL con PostGIS desde:
   -https://postgresapp.com/ (Mac)
   - https://www.enterprisedb.com/downloads/postgres-postgresql-downloads (Windows)
   - Incluir PostGIS extension

3. Configurar GDAL:
   - Instalar OSGeo4W https://trac.osgeo.org/osgeo4w/
   - Agregar `C:\OSGeo4W\bin` al PATH
   - Configurar variable: `GDAL_LIBRARY_PATH=C:\OSGeo4W\bin\gdal302.dll`

#### Mac

```bash
brew install python postgresql postgis gdal
brew services start postgresql
```

### Paso 2: Configurar base de datos

```bash
# Iniciar PostgreSQL
sudo service postgresql start

# Acceder a consola PostgreSQL
sudo -u postgres psql

-- Dentro de psql:
CREATE DATABASE rrhh_db;
\c rrhh_db
CREATE EXTENSION postgis;
\q
```

### Paso 3: Crear entorno virtual

```bash
cd RRHH
python -m venv venv

# Activar
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements/development.txt
```

### Paso 4: Variables de entorno

```bash
cp .env.example .env
```

Editar `.env` con los datos correctos:

```env
DEBUG=True
SECRET_KEY=django-insecure-change-this-please
DB_NAME=rrhh_db
DB_USER=postgres
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=5432
GDAL_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu/libgdal.so  # Ajustar para tu OS
```

### Paso 5: Migraciones y datos iniciales

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py migrate --run-syncdb

# Crear superusuario
python manage.py createsuperuser
# Seguir prompts
# Username: admin
# Email: admin@institucion.gov.py
# Password: [ingresar]
```

### Paso 6: Recolectar archivos estáticos

```bash
python manage.py collectstatic --noinput
```

### Paso 7: Servidor de desarrollo

```bash
python manage.py runserver
```

Acceder a http://localhost:8000/dashboard/

---

## Configuración Post-Instalación

### 1. Crear primeros usuarios

Login como admin en http://localhost:8000/admin/

Crear usuario con rol RRHH:

1. Ir a "Usuarios" -> "Añadir usuario"
2. Llenar datos: username, password, CI, cargo, etc.
3. En "Rol" seleccionar "RRHH"
4. Guardar

### 2. Configurar datos de la institución (Opcional)

Editar `config/settings/base.py`:

```python
# Logo institucional
# Agregar logo en templates/base/base.html

# Colores institucionales
# Modificar CSS en static/css/custom.css
```

### 3. Configurar email (Opcional)

En `.env`:

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-correo@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password
DEFAULT_FROM_EMAIL=sistema@institucion.gov.py
```

### 4. Backup automático (Producción)

Configurar cron job:

```bash
# Ejemplo: Backup diario a las 2 AM
0 2 * * * docker-compose exec db pg_dump -U postgres rrhh_db > /backup/rrhh_$(date +\%Y\%m\%d).sql
```

---

## Solución de Problemas

### Error: "FATAL: password authentication failed for user "postgres""

Verificar contraseña en `.env` y en PostgreSQL.

```bash
# Cambiar contraseña PostgreSQL
sudo -u postgres psql
ALTER USER postgres PASSWORD 'postgres123';
```

### Error: "Could not find the GDAL library"

#### Linux

```bash
sudo apt-get install gdal-bin libgdal-dev
# En settings/base.py ya debería detectar automáticamente
```

#### Windows

```env
# En .env
GDAL_LIBRARY_PATH=C:\OSGeo4W\bin\gdal302.dll
```

Verificar con:
```bash
python -c "from django.contrib.gis import gdal; print(gdal.HAS_GDAL)"
```

### Error: "relation does not exist"

Las migraciones no se ejecutaron correctamente.

```bash
python manage.py migrate --run-syncdb
```

### Error: "permission denied for relation django_migrations"

```bash
sudo -u postgres psql rrhh_db -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;"
```

### Puerto 8000 ocupado

```bash
# Cambiar puerto
python manage.py runserver 8080
```

O en docker-compose.yml:
```yaml
ports:
  - "8080:8000"
```

### Contenedores no inician

```bash
# Reconstruir
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### GDAL Library Path en Docker

Si falla GDAL en Docker, verificar:

```bash
docker-compose exec web python -c "from django.contrib.gis import gdal; print(gdal.HAS_GDAL)"
```

Debe devolver `True`. Si no, verificar el Dockerfile tenga:

```dockerfile
RUN apt-get install -y gdal-bin libgdal-dev
```

---

## Verificación de Instalación

### 1. Verificar PostGIS

```bash
docker-compose exec db psql -U postgres -d rrhh_db -c "SELECT PostGIS_version();"
```

Debe devolver versión de PostGIS.

### 2. Verificar aplicación Django

```bash
docker-compose exec web python manage.py check
```

### 3. Verificar API

```bash
curl http://localhost:8000/api/personas/
# Debe devolver array JSON (autenticación requerida)
```

### 4. Verificar mapa

1. Ir a http://localhost:8000/personas/mapa/
2. Debería cargar mapa con marcadores (si hay domicilios registrados)

---

## Desinstalación

### Docker

```bash
# Detener y eliminar contenedores
docker-compose down

# Eliminar volúmenes (datos se pierden)
docker-compose down -v

# Eliminar imágenes
docker rmi rrhh_web
docker rmi postgis/postgis
```

### Manual

```bash
# Eliminar base de datos
sudo -u postgres dropdb rrhh_db

# Eliminar entorno virtual
rm -rf venv/

# Eliminar archivos estáticos
rm -rf staticfiles/
rm -rf media/
```

---

## Próximos Pasos

1. Personalizar templates con logo institucional
2. Configurar dominios y SSL en producción
3. Establecer backup automático
4. Configurar monitoring (Sentry, etc.)
5. Revisar ajustes de performance

---

## Soporte

Consultar README.md principal o abrir issue en repositorio.
