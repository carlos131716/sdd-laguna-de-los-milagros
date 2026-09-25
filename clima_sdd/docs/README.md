# SDD — Sistema de Consulta del Clima y Turismo

Este es el índice único de requisitos y decisiones técnicas. La aplicación es un monolito Flask modularizado: backend, frontend, persistencia y predicción están separados por responsabilidad.

## Estándar y trazabilidad

- [Estándar de SDD](sdd/00-estandar-sdd.md)
- [Matriz consolidada](sdd/13-matriz-trazabilidad.md)
- [Despliegue AWS EC2](sdd/14-despliegue-aws-ec2.md)

## Estado de capacidades

| Área | Estado | Documento |
|---|---|---|
| Consulta meteorológica | Implementado | [01-clima.md](sdd/01-clima.md) |
| Registro y autenticación | Implementado | [02-autenticacion.md](sdd/02-autenticacion.md) |
| UX y frontend | Implementado | [03-ux.md](sdd/03-ux.md) |
| Seguridad | Base implementada | [04-seguridad.md](sdd/04-seguridad.md) |
| Calidad y pruebas | Implementado | [05-calidad.md](sdd/05-calidad.md) |
| Operación | Base implementada | [06-operacion.md](sdd/06-operacion.md) |
| Roadmap general | Pendiente por fases | [07-roadmap.md](sdd/07-roadmap.md) |
| Catálogo turístico | Implementado con un lugar | [08-turismo.md](sdd/08-turismo.md) |
| Predicción de visitas | Modelo v0 explicable | [09-prediccion-visitas.md](sdd/09-prediccion-visitas.md) |
| Datos turísticos | Diseño futuro | [10-datos-turismo.md](sdd/10-datos-turismo.md) |
| API turística | HTML actual, JSON futuro | [11-api-turismo.md](sdd/11-api-turismo.md) |
| Operación turística | Diseño | [12-operacion-turismo.md](sdd/12-operacion-turismo.md) |

## Arquitectura actual

- Backend: `app.py`, `backend/` y `weather_service.py`.
- Frontend: `frontend/templates/` y `frontend/static/`.
- Base de datos: `backend/database.py` y `database/schema.sql`.
- Pruebas: `tests/`.

## Módulo turístico inicial

El catálogo inicia con la Laguna de los Milagros, reportada por MINCETUR 2024 en Huánuco, provincia de Leoncio Prado, distrito de Pueblo Nuevo, según la ficha de [MINCETUR](https://consultasenlinea.mincetur.gob.pe/fichaInventario/index.aspx?cod_Ficha=4858). La predicción usa la base anual oficial de 57,465 visitantes y clima en tiempo real; no debe presentarse como conteo real del día.

## Principios

1. El dominio no debe depender de detalles de Open-Meteo.
2. Autenticación, clima, turismo y persistencia deben evolucionar de forma independiente.
3. Toda entrada se valida antes de tocar servicios externos o la base de datos.
4. La configuración y los secretos llegan por variables de entorno.
5. Toda nueva capacidad requiere SDD, pruebas y criterios de aceptación.
6. Una observación real nunca se mezcla con una predicción.

## Matriz de trazabilidad

| Requisito | Implementación | Verificación |
|---|---|---|
| RF-01–RF-15 Consulta | `backend/weather_routes.py`, `weather_service.py`, `frontend/templates/index.html` | `tests/test_app.py`, `tests/test_weather_service.py` |
| AUTH-01–AUTH-08 Cuenta | `backend/auth.py`, vistas de `frontend/templates/` | `tests/test_auth.py` |
| TUR-01–TUR-05 Catálogo | `backend/tourism.py`, `backend/tourism_routes.py` | `tests/test_tourism.py` |
| PRED-01–PRED-05 Estimación | `backend/tourism.py`, `frontend/templates/tourism/detail.html` | `tests/test_tourism.py` |
| SEC-01–SEC-07 Seguridad | `backend/config.py`, sesiones y hash | `tests/test_auth.py` |

## Fuente única de verdad

La documentación vigente está únicamente en `docs/sdd/`. La especificación monolítica anterior fue eliminada para evitar requisitos duplicados o desactualizados.
