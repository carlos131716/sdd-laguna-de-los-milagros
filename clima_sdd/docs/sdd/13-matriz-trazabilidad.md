# SDD-013 — Matriz consolidada de trazabilidad

## Requisitos por módulo

| ID | Módulo | Descripción | Implementación | Prueba |
|---|---|---|---|---|
| RF-CLI-01..08 | Clima | Entrada, proveedor, normalización y errores | `backend/weather_routes.py`, `weather_service.py` | `test_app.py`, `test_weather_service.py` |
| RF-AUTH-01..09 | Auth | Cuenta, sesión y protección | `backend/auth.py` | `test_auth.py` |
| RF-UX-01..07 | Frontend | Navegación, semántica y accesibilidad | `frontend/` | Integración + revisión manual |
| TUR-01..05 | Turismo | Catálogo y detalle | `backend/tourism.py`, `tourism_routes.py` | `test_tourism.py` |
| PRED-01..05 | Predicción | Base oficial, ajuste climático y disclaimer | `backend/tourism.py` | `test_tourism.py` |
| SEC-01..08 | Seguridad | Sesión, secretos, entrada y privacidad | `backend/config.py`, `auth.py` | `test_auth.py` + revisión |
| OPS-01..06 | Operación | Health, logs, timeout y recuperación | `app.py`, Docker, configuración | Checklist de despliegue |
| DEPLOY-01..08 | AWS EC2 | Instancia, red, Docker, persistencia y rollback | `docs/sdd/14-despliegue-aws-ec2.md` | Verificación manual en EC2 |

## Requisitos no funcionales globales

| ID | Objetivo | Verificación |
|---|---|---|
| NFR-01 | P95 normal menor a 5 segundos | Prueba de carga |
| NFR-02 | Sin dependencia de Internet en tests | Suite pytest |
| NFR-03 | Sin secretos versionados | Revisión y scanner |
| NFR-04 | No scroll horizontal en móvil | Revisión responsive |
| NFR-05 | Errores externos controlados | Tests con mocks |
| NFR-06 | Predicción identificada como estimación | Test de template |

## Gates de entrega

1. El SDD está actualizado.
2. La matriz tiene implementación y prueba.
3. `pytest -q` pasa.
4. No hay datos personales o secretos en el repositorio.
5. Se documentan limitaciones y deuda técnica.
