# SDD-005 — Calidad y pruebas

## Metadata

| Campo | Valor |
|---|---|
| Version | 2.0 |
| Estado | Implementado |
| Comando | `pytest -q` |
| Dependencia externa | Ninguna durante pruebas |

## Estrategia

### Unitarias

Validan reglas puras: ciudad, email, códigos meteorológicos, catálogo turístico y cálculo de visitantes.

### Integración

Prueban rutas Flask con SQLite temporal, sesión autenticada y proveedor HTTP mockeado.

### E2E futura

Probará registro → login → consulta clima → turismo → detalle → logout en un navegador real.

## Matriz de suites

| Suite | Responsabilidad | Riesgos cubiertos |
|---|---|---|
| `test_app.py` | Clima y rutas protegidas | Validación, errores, reemplazo de resultados |
| `test_auth.py` | Identidad y sesión | Registro, login, logout, duplicados, redirect |
| `test_weather_service.py` | Open-Meteo | Timeout, JSON incompleto, ciudad inexistente |
| `test_tourism.py` | Turismo y predicción | Catálogo, base 2024, estimación visible |

## Requisitos de calidad

- QA-01: las pruebas no deben usar Internet.
- QA-02: cada requisito nuevo debe tener al menos un caso positivo y uno negativo.
- QA-03: los errores externos deben probarse con mocks.
- QA-04: los tests deben ser repetibles y aislar su base temporal.
- QA-05: CI debe bloquear cambios si falla `pytest -q`.
- QA-06: cobertura objetivo inicial de 80% para backend.

## Criterios de aceptación

La capacidad se considera terminada cuando las pruebas pasan, el criterio manual principal se verifica y el SDD contiene contrato, errores y trazabilidad.

## Próximos controles

Agregar cobertura, Ruff o equivalente, Bandit, escaneo de dependencias, Playwright, auditoría WCAG y pruebas de carga para proveedor y predicción.
