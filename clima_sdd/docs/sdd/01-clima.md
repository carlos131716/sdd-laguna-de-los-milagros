# SDD-001 — Consulta meteorologica

## Metadata

| Campo | Valor |
|---|---|
| Version | 2.0 |
| Estado | Implementado |
| Prioridad | Alta |
| Responsable | Backend / Integracion externa |
| Dependencias | Open-Meteo, sesion autenticada |

## Objetivo y usuarios

Un usuario autenticado ingresa una ciudad y recibe el estado meteorologico actual en una respuesta comprensible. El sistema debe seguir funcionando aunque Open-Meteo falle.

## Alcance

Incluye geocodificacion, consulta actual, normalizacion del modelo interno, traduccion de codigos y mensajes de error. No incluye pronostico diario, favoritos, historico ni alertas.

## Requisitos funcionales

- RF-CLI-01: mostrar campo de ciudad y boton de consulta.
- RF-CLI-02: limpiar espacios y rechazar vacio, menos de 2 o mas de 100 caracteres.
- RF-CLI-03: buscar la primera coincidencia de geocodificacion en español.
- RF-CLI-04: consultar temperatura, humedad, viento y codigo actual.
- RF-CLI-05: traducir el codigo meteorologico a una descripcion en español.
- RF-CLI-06: mostrar ciudad, pais, temperatura, clima, humedad y viento.
- RF-CLI-07: no conservar resultado anterior cuando falla una nueva consulta.
- RF-CLI-08: ocultar detalles tecnicos y registrar la excepcion en servidor.

## Requisitos no funcionales

- RNF-CLI-01: timeout externo de 5 segundos.
- RNF-CLI-02: el proveedor externo no debe detener el proceso Flask.
- RNF-CLI-03: el contrato interno no debe depender de nombres de Open-Meteo.
- RNF-CLI-04: todas las unidades mostradas deben ser explicitas.
- RNF-CLI-05: la respuesta normal debe ser menor a 5 segundos bajo condiciones normales.

## Flujo principal

`POST /` → validar → geocodificar → consultar coordenadas → normalizar → renderizar.

## Rutas

| Metodo | Ruta | Acceso | Resultado |
|---|---|---|---|
| GET | `/` | Autenticado | Formulario |
| POST | `/` | Autenticado | Resultado o error |
| POST | `/clima` | Autenticado | Alias del flujo principal |

## Contrato interno

```python
{
  "ciudad": str, "pais": str, "temperatura": float,
  "descripcion": str, "humedad": float,
  "viento": float, "unidad_viento": str
}
```

## Errores

| Situacion | Excepcion | Mensaje |
|---|---|---|
| Entrada vacia | Validacion | Ingrese el nombre de una ciudad. |
| Ciudad no encontrada | `CityNotFoundError` | Ciudad no encontrada. |
| Timeout o red | `WeatherServiceError` | No se pudo obtener la informacion del clima. |
| Campos incompletos | `WeatherServiceIncompleteError` | La informacion no esta disponible. |
| Error inesperado | Excepcion generica | Ocurrio un problema. |

## Criterios de aceptacion

```gherkin
Scenario: consulta correcta
  Given un usuario autenticado
  When consulta "Tingo Maria"
  Then ve temperatura, clima, humedad y viento

Scenario: proveedor no disponible
  Given Open-Meteo devuelve timeout
  When consulta una ciudad
  Then ve un mensaje controlado y la aplicación sigue disponible
```

## Implementacion y pruebas

- Codigo: `backend/weather_routes.py`, `backend/weather_validation.py`, `weather_service.py`.
- Frontend: `frontend/templates/index.html`.
- Pruebas: `tests/test_app.py`, `tests/test_weather_service.py`.

## Riesgos y evolucion

El proveedor puede cambiar contrato o limites. La siguiente iteracion debe extraer `WeatherProvider`, añadir cache TTL, rate limit por usuario y pronostico como caso de uso independiente.
