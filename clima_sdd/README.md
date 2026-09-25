# Sistema Web de Consulta del Clima

Aplicación Flask para consultar el clima actual de una ciudad mediante Open-Meteo. Incluye registro, login, sesiones y persistencia local SQLite.

## Estructura

```text
.
├── app.py
├── backend/
├── database/schema.sql
├── frontend/
│   ├── templates/
│   └── static/
├── weather_service.py
├── tests/
└── docs/
```

La arquitectura detallada está en [docs/ARQUITECTURA.md](docs/ARQUITECTURA.md) y los requisitos en [docs/README.md](docs/README.md).

## Instalación

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Ejecución

```bash
python app.py
```

Abre `http://127.0.0.1:5000/registro` para crear la primera cuenta.

## Pruebas

```bash
pytest -q
```

## Docker

```bash
docker build -t clima-sdd .
docker run --rm -p 5000:5000 clima-sdd
```

## Configuración

Usa `.env.example` como referencia. En producción define un `SECRET_KEY` aleatorio, activa `SESSION_COOKIE_SECURE=1` y usa una base de datos persistente.
