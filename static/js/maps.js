/**
 * Maps.js - Funciones auxiliares para mapas
 * Sistema RRHH - Gestión de Funcionarios
 */

(function() {
    'use strict';

    // Variables globales del mapa
    window.rrhhMap = null;
    window.geojsonLayer = null;

    /**
     * Inicializar mapa Leaflet
     * @param {string} elementId - ID del contenedor del mapa
     * @param {Array} center - Coordenadas [lat, lng] para centrar
     * @param {number} zoom - Nivel de zoom inicial
     */
    function initMap(elementId, center, zoom) {
        if (!elementId) elementId = 'map';

        const mapElement = document.getElementById(elementId);
        if (!mapElement) {
            console.error('Elemento del mapa no encontrado:', elementId);
            return null;
        }

        // Crear mapa
        window.rrhhMap = L.map(elementId).setView(center, zoom);

        // Añadir capa OpenStreetMap
        L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            maxZoom: 19
        }).addTo(window.rrhhMap);

        return window.rrhhMap;
    }

    /**
     * Cargar GeoJSON desde API
     * @param {string} url - URL del endpoint GeoJSON
     * @param {Object} filters - Filtros a aplicar
     * @param {string} markersStyle - Clase CSS para marcadores personalizados
     */
    function loadGeoJSON(url, filters = {}, markersStyle = 'default') {
        if (!window.rrhhMap) {
            console.error('Mapa no inicializado. Ejecute initMap() primero.');
            return;
        }

        // Construir URL con query params
        const params = new URLSearchParams();
        Object.keys(filters).forEach(key => {
            if (filters[key] !== undefined && filters[key] !== '') {
                params.append(key, filters[key]);
            }
        });

        const fullUrl = params.toString() ? `${url}?${params.toString()}` : url;

        fetch(fullUrl)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                // Remover capa anterior
                if (window.geojsonLayer) {
                    window.rrhhMap.removeLayer(window.geojsonLayer);
                }

                // Crear marcadores
                window.geojsonLayer = L.geoJSON(data, {
                    pointToLayer: function(feature, latlng) {
                        return createMarker(latlng, markersStyle);
                    },
                    onEachFeature: function(feature, layer) {
                        bindPopup(layer, feature.properties);
                    }
                }).addTo(window.rrhhMap);

                // Ajustar vista a marcadores
                if (data.features && data.features.length > 0) {
                    const bounds = window.geojsonLayer.getBounds();
                    window.rrhhMap.fitBounds(bounds, { padding: [50, 50], maxZoom: 13 });
                }
            })
            .catch(error => {
                console.error('Error cargando GeoJSON:', error);
                showAlert('Error al cargar los datos del mapa.', 'danger');
            });
    }

    /**
     * Crear marcador personalizado
     */
    function createMarker(latlng, style) {
        let color = '#0d6efd';
        let size = 12;

        switch (style) {
            case 'active':
                color = '#198754';
                break;
            case 'inactive':
                color = '#dc3545';
                break;
            default:
                color = '#0d6efd';
        }

        return L.marker(latlng, {
            icon: L.divIcon({
                className: 'rrhh-marker',
                html: `<div style="background-color: ${color}; width: ${size}px; height: ${size}px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.3);"></div>`,
                iconSize: [size + 6, size + 6],
                iconAnchor: [(size + 6) / 2, (size + 6) / 2],
                popupAnchor: [0, -(size + 6) / 2]
            })
        });
    }

    /**
     * Vincular popup a marcador
     */
    function bindPopup(layer, properties) {
        const popupContent = createPopupContent(properties);
        layer.bindPopup(popupContent);
    }

    /**
     * Crear contenido HTML del popup
     */
    function createPopupContent(props) {
        let html = `
            <div class="rrhh-popup p-2" style="min-width: 180px;">
                <h6 class="mb-2">${props.persona_nombre || 'Sin nombre'}</h6>
                <small>
        `;

        if (props.persona_ci) {
            html += `<strong>CI:</strong> ${props.persona_ci}<br>`;
        }
        if (props.DIRECCION) {
            html += `<strong>Dirección:</strong> ${props.DIRECCION}<br>`;
        }
        if (props.BARRIO) {
            html += `<strong>Barrio:</strong> ${props.BARRIO}<br>`;
        }
        if (props.CIUDAD) {
            html += `<strong>Ciudad:</strong> ${props.CIUDAD}<br>`;
        }

        html += `
                </small>
                <div class="mt-2">
                    <a href="/personas/${props.persona}/" class="btn btn-sm btn-primary">Ver Ficha</a>
                </div>
            </div>
        `;

        return html;
    }

    /**
     * Mostrar alerta
     */
    function showAlert(message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        const container = document.querySelector('.container-fluid') || document.body;
        container.insertBefore(alertDiv, container.firstChild);

        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }

    // Exportar funciones al ámbito global
    window.RHHMaps = {
        initMap,
        loadGeoJSON,
        showAlert
    };

})();
