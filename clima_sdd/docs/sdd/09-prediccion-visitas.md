# SDD-009 — Predicción diaria de visitantes

## Objetivo

Estimar visitantes diarios para la Laguna de los Milagros combinando la base oficial 2024 de MINCETUR con el clima actual.

## Base oficial integrada

MINCETUR registra para 2024:

- 1,426 turistas extranjeros.
- 13,050 turistas nacionales.
- 42,989 visitantes locales.
- **Total anual: 57,465 visitantes.**

La línea base diaria es `57,465 / 366 = 157 visitantes por día`.

## Modelo climático v1

Parte de la línea base diaria y aplica multiplicadores explicables por temperatura, código meteorológico, humedad y viento. El resultado es una predicción diaria calibrada, no un conteo observado.

## Salida

```python
{
  "estimated_visitors": int,
  "baseline_daily": float,
  "annual_total_2024": int,
  "confidence": str,
  "factors": list[str],
  "is_observed": False,
  "model_version": "climate-v1"
}
```

## Criterios de aceptación

1. La pantalla muestra la cifra oficial 2024 y su desglose conceptual.
2. La pantalla diferencia visitantes observados de visitantes estimados.
3. Una condición favorable produce una estimación mayor que una tormenta.
4. La predicción muestra los factores que la explican.
5. Si falla el proveedor climático, no se muestra una predicción engañosa.

## Limitaciones

La base es anual, no mensual ni diaria. Para mejorar el modelo se necesitan registros por fecha, feriados, eventos, vacaciones y cierres.
