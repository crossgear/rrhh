# Dockerfile para Sistema RRHH
FROM python:3.11-slim

# Evitar que Python escriba archivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar dependencias del sistema necesarias para GDAL y PostgreSQL
RUN apt-get update && apt-get install -y --no-install-recommends \
    gdal-bin \
    libgdal-dev \
    libgeos-dev \
    proj-bin \
    proj-data \
    libproj-dev \
    gcc \
    postgresql-client \
    build-essential \
    libldap2-dev \
    libsasl2-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Instalar dependencias Python
COPY requirements/ /app/requirements/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements/production.txt

# Copiar proyecto
COPY . /app/

# Crear directorios necesarios
# Crear directorios necesarios
RUN mkdir -p /app/logs /app/media/fotos_carnet && chmod -R 755 /app/logs && chmod -R 777 /app/media && touch /app/logs/rrhh.log && chown -R www-data:www-data /app/logs /app/media

# Recolectar archivos estáticos
RUN python manage.py collectstatic --noinput --clear

# Crear usuario no-root para ejecutar
RUN chown -R www-data:www-data /app

# USER www-data

# Exponer puerto
EXPOSE 8000

# Comando de ejecución
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
