# SDD-011 — API del módulo turístico

## Metadata

| Campo | Valor |
|---|---|
| Version | 2.0 |
| Estado | Vistas HTML implementadas; API JSON planificada |
| Autenticación | Sesión actual; token futuro |
| Versionado futuro | `/api/v1` |

## Contratos actuales

- `GET /turismo`: lista HTML de lugares activos.
- `GET /turismo/<slug>`: detalle HTML, clima, base oficial y predicción.
- Ambos endpoints requieren usuario autenticado.

## Contratos JSON futuros

```http
GET /api/v1/tourist-places
GET /api/v1/tourist-places/{slug}
GET /api/v1/tourist-places/{slug}/visitor-estimate
```

Ejemplo de respuesta de estimación:

```json
{
  "place": "laguna-de-los-milagros",
  "observed_year": 2024,
  "annual_observed_visitors": 57465,
  "estimated_today": 182,
  "confidence": "Baja",
  "is_observed": false,
  "model_version": "climate-v1",
  "generated_at": "2026-09-25T12:00:00Z"
}
```

## Errores

| HTTP | Caso |
|---:|---|
| 401 | Sesión o token ausente |
| 404 | Lugar inexistente |
| 422 | Parámetro inválido |
| 502 | Proveedor meteorológico no disponible |
| 503 | Servicio temporalmente no disponible |

## Compatibilidad

No romper las vistas HTML al introducir JSON. Los campos `is_observed`, `confidence` y `model_version` son obligatorios para evitar que una predicción se interprete como dato oficial.

## Seguridad y límites

Aplicar CSRF en sesión, rate limiting, paginación del catálogo, límite de tamaño de respuesta y logging de request id sin datos sensibles.
