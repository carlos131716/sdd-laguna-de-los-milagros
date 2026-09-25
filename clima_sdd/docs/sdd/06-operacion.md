# SDD-006 — Operacion y despliegue

## Metadata

| Campo | Valor |
|---|---|
| Version | 2.0 |
| Estado | MVP operativo |
| Runtime | Python 3.12, Flask |
| Persistencia | SQLite local |
| Contenedor | Docker |

## Configuración

| Variable | Obligatoria en producción | Uso |
|---|---|---|
| `SECRET_KEY` | Si | Firma de sesión |
| `DATABASE_PATH` | Recomendada | Ruta SQLite |
| `SESSION_COOKIE_SECURE` | Si | Cookies solo HTTPS |
| `PORT` | No | Puerto HTTP |
| `FLASK_RUN_HOST` | No | Host de escucha |

## Arranque

1. `app.py` llama a `create_app()`.
2. La fábrica carga configuración.
3. Registra hooks, autenticación, clima y turismo.
4. Inicializa la tabla `users`.
5. Flask sirve `frontend/templates` y `frontend/static`.

## Despliegue actual

Docker usa `python:3.12-slim`, instala dependencias fijadas y expone el puerto 5000. SQLite requiere volumen persistente. La semilla turística `database/mincetur_2024.csv` se distribuye como archivo versionado de referencia oficial.

## Requisitos operativos

- OPS-01: healthcheck de aplicación y base.
- OPS-02: logs con timestamp, ruta, status y duración.
- OPS-03: no escribir secretos en logs.
- OPS-04: timeout en todos los proveedores externos.
- OPS-05: backup y restauración probados para datos persistidos.
- OPS-06: monitorear errores y latencia de Open-Meteo.

## Producción recomendada

Gunicorn detrás de TLS, PostgreSQL con Alembic, Redis para cache/rate limit, secretos administrados, CI/CD, métricas, trazas y backups automáticos.

## Recuperación

Ante caída de Open-Meteo se debe mostrar error controlado. Ante corrupción de SQLite se restaura backup y se valida el esquema. Ante una predicción anómala se conserva el `model_version` y se desactiva el modelo antes de corregirlo.
