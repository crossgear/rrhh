#!/bin/bash
#
# Script de inicialización del sistema RRHH
# Ejecutar después de clonar el proyecto
#

set -e  # Salir en caso de error

echo "=== Inicializando Sistema RRHH ==="

# Verificar entorno virtual
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  No se detectó entorno virtual. Se recomienda activarlo antes de continuar."
    echo "   python -m venv venv"
    echo "   source venv/bin/activate  (Linux/Mac)"
    echo "   venv\\Scripts\\activate   (Windows)"
fi

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install -r requirements/development.txt

# Variables de entorno
if [ ! -f .env ]; then
    echo "⚙️  Creando archivo .env desde .env.example..."
    cp .env.example .env
    echo "   ⚠️  IMPORTANTE: Edite .env con la configuración real de su entorno"
fi

# Configuración Docker
echo "🐳 Configurando Docker..."
if command -v docker-compose &> /dev/null; then
    echo "   Iniciando servicios PostgreSQL+PostGIS..."
    docker-compose up -d db

    echo "   Esperando a que la base de datos esté lista..."
    sleep 10
else
    echo "   ⚠️  Docker Compose no encontrado. Configure PostgreSQL manualmente."
fi

# Migraciones
echo "🗃️  Aplicando migraciones..."
python manage.py makemigrations
python manage.py migrate
python manage.py migrate --run-syncdb

# Superusuario
echo "👤 Creando superusuario..."
python manage.py shell -c "
from apps.usuarios.models import Usuario
if not Usuario.objects.filter(username='admin').exists():
    Usuario.objects.create_superuser(
        username='admin',
        email='admin@institucion.gov.py',
        password='admin123',
        CI='12345678',
        CARGO='Administrador del Sistema',
        ROL='ADMIN'
    )
    print('✅ Superusuario creado: admin / admin123')
else:
    print('⚠️  Superusuario ya existe')
"

# Archivos estáticos
echo "📁 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo ""
echo "=== Inicialización Completada ==="
echo ""
echo "📍 Para iniciar el servidor de desarrollo:"
echo "   python manage.py runserver"
echo ""
echo "📍 O usando Docker:"
echo "   docker-compose up -d web"
echo ""
echo "🌐 Accesos:"
echo "   - Frontend:  http://localhost:8000/dashboard/"
echo "   - API:       http://localhost:8000/api/"
echo "   - Admin:     http://localhost:8000/admin/"
echo ""
echo "👤 Credenciales por defecto:"
echo "   Usuario: admin"
echo "   Contraseña: admin123"
echo ""
echo "⚡ ¡El sistema está listo para usar!"
