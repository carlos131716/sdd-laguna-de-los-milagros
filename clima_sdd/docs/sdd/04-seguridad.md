# SDD-004 — Seguridad y privacidad

## Metadata

| Campo | Valor |
|---|---|
| Version | 2.0 |
| Estado | Base implementada; endurecimiento pendiente |
| Datos sensibles | Credenciales y sesiones |
| Riesgo principal | Robo de sesión, abuso de formularios y fuerza bruta |

## Controles implementados

- Hash adaptativo de contraseñas con Werkzeug.
- Consultas SQL parametrizadas.
- Cookie HTTP-only y SameSite Lax.
- `SECRET_KEY` configurable por entorno.
- Validación de `next` contra redirecciones externas.
- Errores internos registrados sin mostrar trazas.
- Base SQLite excluida del control de versiones.

## Requisitos de seguridad

- SEC-01: no almacenar secretos en el repositorio.
- SEC-02: no escribir contraseñas, tokens ni hashes en logs.
- SEC-03: proteger todas las rutas privadas con `login_required`.
- SEC-04: utilizar HTTPS en producción.
- SEC-05: activar `SESSION_COOKIE_SECURE=1` en producción.
- SEC-06: validar y limitar toda entrada del usuario.
- SEC-07: aislar fallos de proveedores externos.
- SEC-08: definir retención y borrado de datos turísticos.

## Amenazas y controles

| Amenaza | Impacto | Control actual | Próximo control |
|---|---|---|---|
| Fuerza bruta | Alto | Mensaje genérico | Rate limiting y backoff |
| Robo de sesión | Alto | HTTP-only, SameSite | HTTPS, expiración y rotación |
| CSRF | Alto | Pendiente | Token CSRF en POST |
| SQL injection | Alto | Parametrización | Revisión SAST |
| Open redirect | Medio | Validación de `next` | Prueba de seguridad automatizada |
| Abuso API clima | Medio | Timeout | Cache y rate limit por usuario |
| Datos falsos de predicción | Medio | Disclaimer y `is_observed` | Versionado y auditoría del modelo |

## Privacidad

El sistema debe guardar solo el email y datos agregados de visitas. No debe registrar identidad de turistas individuales sin una especificación legal y de privacidad separada.

## Criterios de aceptación

1. Una contraseña no aparece en base, HTML, logs ni errores.
2. Un usuario anónimo no accede a clima ni turismo.
3. Un `next` externo no redirige fuera de la aplicación.
4. Un fallo externo no revela URLs internas ni trazas.

## Producción

Usar secretos administrados, dependencia escaneada, backups cifrados, rotación de credenciales, headers de seguridad, auditoría y un procedimiento probado de respuesta a incidentes.
