# SDD-002 — Registro y autenticacion

## Metadata

| Campo | Valor |
|---|---|
| Version | 2.0 |
| Estado | Implementado con controles pendientes |
| Prioridad | Critica |
| Actor principal | Usuario |
| Persistencia | SQLite, tabla `users` |

## Objetivo

Crear una identidad minima para proteger consultas y futuras preferencias del usuario.

## Requisitos funcionales

- RF-AUTH-01: permitir registro con email y contraseña.
- RF-AUTH-02: normalizar email a minusculas.
- RF-AUTH-03: rechazar contraseña menor de 8 caracteres.
- RF-AUTH-04: rechazar email duplicado.
- RF-AUTH-05: autenticar con mensaje generico si falla cualquier credencial.
- RF-AUTH-06: crear sesion despues de autenticacion correcta.
- RF-AUTH-07: redirigir rutas protegidas a `/login`.
- RF-AUTH-08: limpiar sesion mediante `POST /logout`.
- RF-AUTH-09: validar `next` para permitir solo rutas locales.

## Requisitos no funcionales

- RNF-AUTH-01: nunca guardar contraseñas en texto plano.
- RNF-AUTH-02: usar hash adaptativo de Werkzeug.
- RNF-AUTH-03: cookie HTTP-only y SameSite Lax.
- RNF-AUTH-04: no exponer si un email existe mediante mensajes diferentes en login.
- RNF-AUTH-05: permitir reemplazar SQLite por PostgreSQL sin cambiar las rutas.

## Modelo de datos actual

```sql
users(
  id INTEGER PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  created_at TEXT NOT NULL
)
```

## Contrato de rutas

| Metodo | Ruta | Entrada | Salida |
|---|---|---|---|
| GET | `/registro` | — | Formulario |
| POST | `/registro` | email, password | Redirect a login o errores |
| GET | `/login` | — | Formulario |
| POST | `/login` | email, password, next opcional | Sesion o error |
| POST | `/logout` | Cookie de sesion | Sesion invalidada |

## Estados y errores

- Email invalido: error de formulario.
- Contraseña corta: error de formulario.
- Cuenta duplicada: error de formulario.
- Credenciales invalidas: mensaje generico.
- Sesion ausente: redirect 302 a login.

## Criterios de aceptacion

```gherkin
Scenario: registro y login
  Given no existe el email
  When envia email valido y contraseña de 8 caracteres o mas
  Then se crea el usuario y puede iniciar sesion

Scenario: acceso protegido
  Given un visitante anonimo
  When solicita `/`
  Then es redirigido a `/login`

Scenario: open redirect
  Given un next externo
  When el usuario inicia sesion
  Then aterriza en `/` y no en el dominio externo
```

## Implementacion y pruebas

- Codigo: `backend/auth.py`, `backend/database.py`, `backend/config.py`.
- Vistas: `frontend/templates/login.html`, `frontend/templates/register.html`.
- Pruebas: `tests/test_auth.py` y flujos autenticados de `tests/test_app.py`.

## Pendientes de produccion

CSRF, expiracion y rotacion de sesiones, rate limiting, bloqueo progresivo, recuperacion de contraseña, verificacion de email, MFA, auditoria y migracion con Alembic.
