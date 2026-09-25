"""Punto de entrada compatible para ejecutar la aplicación Flask."""

import os

import weather_service

from backend.app_factory import create_app
from backend.database import get_db as _get_db
from backend.database import init_db as _init_db
from backend.weather_validation import validate_city


app = create_app()


def get_db():
    return _get_db(app)


def init_db():
    return _init_db(app)


if __name__ == "__main__":
    app.run(
        host=os.getenv("FLASK_RUN_HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", "5000")),
        debug=os.getenv("FLASK_DEBUG", "1") == "1",
    )
