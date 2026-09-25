# SDD-010 — Datos turísticos y calidad del dato

## Fuente 2024 integrada

La ficha oficial de [MINCETUR para la Laguna de los Milagros](https://consultasenlinea.mincetur.gob.pe/fichaInventario/index.aspx?cod_Ficha=4858) reporta datos de 2024 con fuente de datos de la Municipalidad Distrital de Pueblo Nuevo.

| Tipo | Visitantes |
|---|---:|
| Turistas extranjeros | 1,426 |
| Turistas nacionales | 13,050 |
| Visitantes locales | 42,989 |
| Total | 57,465 |

La copia reproducible de esta semilla está en `database/mincetur_2024.csv`.

## Reglas de calidad

- No mezclar predicciones con observaciones.
- Cada dato debe conservar año, tipo, cantidad y fuente.
- No convertir un total anual en dato diario observado; solo se usa como promedio de referencia.
- Mantener la fuente oficial y la fecha de actualización documentadas.
- Validar coordenadas antes de consultar proveedores climáticos.

## Modelo futuro

```text
tourist_places
  id, slug, name, region, province, district,
  latitude, longitude, description, active

visitor_observations
  id, place_id, observed_at, visitor_count, visitor_type,
  source, quality_status

weather_observations
  id, place_id, observed_at, temperature, humidity,
  wind_speed, weather_code
```

## Privacidad

Guardar conteos agregados. No registrar identidad de visitantes sin un SDD separado y una base legal definida.
