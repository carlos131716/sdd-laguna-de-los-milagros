from flask import render_template

import weather_service

from .auth import login_required
from .tourism import get_place, get_places, predict_visitors


def register_routes(app):
    @app.get("/turismo")
    @login_required
    def tourism_index():
        return render_template("tourism/index.html", places=get_places())

    @app.get("/turismo/<slug>")
    @login_required
    def tourism_detail(slug):
        place = get_place(slug)
        if place is None:
            return render_template("404.html", message="Lugar turístico no encontrado."), 404
        try:
            current, units = weather_service.fetch_weather(place["latitude"], place["longitude"])
            weather = {
                "temperature": current["temperature_2m"],
                "humidity": current["relative_humidity_2m"],
                "wind": current["wind_speed_10m"],
                "wind_unit": units.get("wind_speed_10m", "km/h"),
                "description": weather_service.describe_weather(current["weather_code"]),
            }
            official = place["official_2024"]
            annual_total = official["foreign"] + official["national"] + official["local"]
            baseline_daily = annual_total / 366
            prediction = predict_visitors(current, baseline_daily)
            prediction["annual_total_2024"] = annual_total
            prediction["official_breakdown"] = official
            error = None
        except (weather_service.WeatherServiceError, KeyError, TypeError, ValueError):
            weather, prediction = None, None
            error = "No se pudo obtener el clima para calcular la estimación."
        return render_template("tourism/detail.html", place=place, weather=weather, prediction=prediction, error=error)
