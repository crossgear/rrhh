-- Script de inicialización de base de datos PostgreSQL
-- Se ejecuta automáticamente cuando se crea el contenedor

-- Crear extensiones GIS necesarias
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;

-- Comentario
COMMENT ON EXTENSION postgis IS 'PostGIS geometry, geography, and raster spatial types and functions';
COMMENT ON EXTENSION postgis_topology IS 'PostGIS topology spatial types and functions';
