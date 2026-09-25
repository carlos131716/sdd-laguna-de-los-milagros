# SDD-008 — Catálogo de lugares turísticos

## Objetivo

Agregar una sección autenticada para consultar lugares turísticos, su clima y una estimación de visitantes.

## Lugar inicial

- **Nombre:** Laguna de los Milagros
- **Región:** Huánuco
- **Provincia:** Leoncio Prado
- **Distrito reportado por MINCETUR 2024:** Pueblo Nuevo
- **Slug:** `laguna-de-los-milagros`

La ubicación se usa como punto de referencia meteorológico; todavía no representa un perímetro GIS.

## Rutas

- `GET /turismo`: lista de lugares.
- `GET /turismo/<slug>`: detalle, clima y predicción diaria.

Ambas requieren sesión autenticada.

## Criterios de aceptación

1. El usuario autenticado ve la Laguna de los Milagros en el catálogo.
2. El detalle muestra ubicación y condiciones meteorológicas.
3. El detalle muestra la base oficial 2024 y la predicción diaria.
4. Un slug inexistente devuelve HTTP 404 controlado.
5. Agregar otro lugar no requiere modificar la plantilla, solo el catálogo y sus datos.

## Evolución

Migrar el catálogo desde `backend/tourism.py` a una tabla `tourist_places`, incluir imágenes, accesibilidad, actividades, horarios, tarifas y coordenadas validadas.
