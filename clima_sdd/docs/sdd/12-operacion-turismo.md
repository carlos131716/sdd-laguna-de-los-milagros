# SDD-012 — Operación y observabilidad turística

## Metadata

| Campo | Valor |
|---|---|
| Version | 2.0 |
| Estado | Diseño |
| Responsables | Backend, datos y operación |
| Dependencias | Open-Meteo, semilla MINCETUR, SQLite/PostgreSQL futuro |

## Métricas de producto

- Lugares consultados por día.
- Detalles turísticos vistos.
- Predicciones generadas.
- Distribución de estimaciones por rango.
- Diferencia entre predicción y observación cuando exista dato real.

## Métricas técnicas

- P50 y P95 de `/turismo` y detalle.
- Errores y timeout de Open-Meteo.
- Porcentaje de respuestas sin clima.
- Tiempo de lectura de datos MINCETUR.
- Errores de carga del CSV y filas descartadas.

## Alertas

- Más de 5% de errores climáticos en 15 minutos.
- Predicciones sin factores explicativos.
- Estimaciones fuera de un rango operacional configurable.
- CSV ausente, vacío o con duplicados.
- Cambio de esquema sin migración.

## Reproducibilidad

Cada predicción persistida debe guardar modelo, versión, timestamp UTC, coordenadas, entrada climática, línea base usada y fuente de datos. La predicción debe poder recalcularse con el mismo input.

## Operación ante incidentes

1. Si Open-Meteo falla, mostrar error y conservar la última observación solo si está marcada como histórica.
2. Si falla la carga MINCETUR, no iniciar una predicción con base desconocida.
3. Si aparecen valores anómalos, desactivar el modelo y mostrar estado no disponible.
4. Registrar incidente, causa, impacto y recuperación.

## Evolución

Migrar ingestas a un worker, almacenar observaciones en PostgreSQL, usar métricas Prometheus y configurar dashboard de calidad del modelo.
