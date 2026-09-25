# SDD-007 — Roadmap de producto y escalabilidad

## Metadata

| Campo | Valor |
|---|---|
| Version | 2.0 |
| Estado | Planificado |
| Criterio de prioridad | Seguridad, valor de usuario, costo operativo |

## Fase 1 — Fundaciones MVP

- [x] Login, registro y logout.
- [x] Persistencia de usuarios.
- [x] Clima actual.
- [x] Catalogo inicial de un lugar.
- [x] Estimacion v1 con base MINCETUR 2024.
- [ ] CSRF y rate limiting.
- [ ] Healthcheck y logs estructurados.

## Fase 2 — Calidad del dato

- [ ] Importar datos mensuales y diarios de visitantes.
- [ ] Registrar fuente, fecha y calidad de cada observación.
- [ ] Capturar feriados, eventos, vacaciones y cierres.
- [ ] Validar coordenadas y revisar inconsistencias territoriales.
- [ ] Dashboard de observados versus estimados.

## Fase 3 — Producto turístico

- [ ] Historial privado de consultas.
- [ ] Ciudades y lugares favoritos.
- [ ] Pronóstico de 7 días.
- [ ] Selector de unidades y zona horaria.
- [ ] Fichas con imágenes, actividades, acceso y horarios.
- [ ] API JSON versionada.

## Fase 4 — Modelo predictivo

- [ ] Línea base mensual por tipo de visitante.
- [ ] Variables de calendario y demanda.
- [ ] Comparar regresión, Random Forest y series temporales.
- [ ] Validación temporal con MAE y RMSE.
- [ ] Versionar modelos y permitir rollback.

## Fase 5 — Escala

- [ ] PostgreSQL y Alembic.
- [ ] Redis para cache y limites.
- [ ] Worker asíncrono para ingestas.
- [ ] Observabilidad completa.
- [ ] Despliegue horizontal y CDN para frontend.

Cada ítem nuevo requiere un SDD, contrato, migración de datos si aplica, prueba y actualización de [la matriz de trazabilidad](13-matriz-trazabilidad.md).
