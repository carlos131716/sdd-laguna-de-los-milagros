# Arquitectura del proyecto

```text
clima_sdd/
├── app.py                    # Punto de entrada Flask
├── backend/
│   ├── app_factory.py        # Ensamblaje de la aplicación
│   ├── config.py             # Configuración por entorno
│   ├── database.py           # Conexión e inicialización SQLite
│   ├── auth.py               # Registro, login, logout y sesiones
│   ├── weather_routes.py     # Rutas del caso de uso clima
│   └── weather_validation.py # Validación de ciudad
├── weather_service.py        # Integración con Open-Meteo
├── database/
│   └── schema.sql            # Esquema inicial
├── frontend/
│   ├── templates/            # Vistas HTML de Flask
│   └── static/               # CSS del frontend
├── tests/                    # Pruebas automatizadas
└── docs/                     # SDD y decisiones técnicas
```

## Flujo de dependencias

`app.py` → `backend.app_factory` → rutas → servicios → base de datos/proveedor externo.

Las plantillas no contienen lógica de negocio. Las rutas coordinan casos de uso, las validaciones controlan entrada y `weather_service.py` encapsula Open-Meteo. Esta separación permite sustituir SQLite, el proveedor meteorológico o el frontend sin reescribir toda la aplicación.

## Regla contra duplicados

Cada responsabilidad debe tener una sola ubicación. No se deben crear copias de plantillas, estilos, esquemas ni especificaciones fuera de las carpetas indicadas.
