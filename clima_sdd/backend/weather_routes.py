from flask import render_template, request

import weather_service

from .auth import login_required
from .weather_validation import validate_city


def register_routes(app):
    @app.route("/", methods=["GET", "POST"])
    @login_required
    def index():
        weather, error, city = None, None, ""
        if request.method == "POST":
            city, error = validate_city(request.form.get("city", ""))
            if error is None:
                try:
                    weather = weather_service.get_current_weather(city)
                except weather_service.CityNotFoundError:
                    error = "Ciudad no encontrada."
                except weather_service.WeatherServiceIncompleteError:
                    error = "La información del clima no está disponible en este momento."
                except weather_service.WeatherServiceError:
                    error = "No se pudo obtener la información del clima."
                except Exception:
                    app.logger.exception("Unexpected weather query error")
                    error = "Ocurrió un problema. Inténtelo nuevamente."
        return render_template("index.html", city=city, weather=weather, error=error)

    @app.route("/clima", methods=["POST"])
    @login_required
    def clima():
        return index()
