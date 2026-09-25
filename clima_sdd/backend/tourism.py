"""Catálogo turístico y estimación inicial de visitantes."""

import csv
import os


def _load_official_2024():
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "mincetur_2024.csv")
    values = {"foreign": 0, "national": 0, "local": 0, "source": "MINCETUR", "year": 2024}
    type_map = {"turistas_extranjeros": "foreign", "turistas_nacionales": "national", "visitantes_locales": "local"}
    with open(path, newline="", encoding="utf-8") as data_file:
        for row in csv.DictReader(data_file):
            if row["place_slug"] == "laguna-de-los-milagros" and row["year"] == "2024":
                values[type_map[row["visitor_type"]]] += int(row["visitor_count"])
                values["source"] = row["source"]
    return values

PLACES = {
    "laguna-de-los-milagros": {
        "slug": "laguna-de-los-milagros",
        "name": "Laguna de los Milagros",
        "region": "Huánuco",
        "province": "Leoncio Prado",
        "district": "Pueblo Nuevo",
        # Coordenada de referencia del recurso turístico; no es un perímetro GIS.
        "latitude": -9.144951,
        "longitude": -75.995253,
        "description": "Destino natural para disfrutar del paisaje, la flora y actividades recreativas.",
        "official_2024": _load_official_2024(),
    }
}


def get_places():
    return list(PLACES.values())


def get_place(slug):
    return PLACES.get(slug)


def predict_visitors(current, baseline_daily=None):
    """Calcula una estimación referencial basada únicamente en clima actual.

    No representa visitantes observados. El valor base se reemplazará por datos
    históricos cuando existan registros de entradas por fecha.
    """
    temperature = float(current.get("temperature_2m", 24))
    humidity = float(current.get("relative_humidity_2m", 75))
    wind = float(current.get("wind_speed_10m", 10))
    code = int(current.get("weather_code", 3))
    estimate = float(baseline_daily or 157)
    factors = []

    if 20 <= temperature <= 30:
        estimate *= 1.25
        factors.append("temperatura favorable")
    elif temperature < 16 or temperature > 34:
        estimate *= 0.70
        factors.append("temperatura poco favorable")
    else:
        estimate *= 1.05
        factors.append("temperatura moderada")

    if code in (0, 1, 2):
        estimate *= 1.20
        factors.append("cielo despejado o parcialmente nublado")
    elif code in (61, 63, 80, 81):
        estimate *= 0.65
        factors.append("lluvia o chubascos")
    elif code in (65, 82, 95, 96, 99):
        estimate *= 0.35
        factors.append("lluvia intensa o tormenta")
    else:
        estimate *= 0.85
        factors.append("nubosidad o condición variable")

    if humidity > 90:
        estimate *= 0.85
        factors.append("humedad muy alta")
    if wind > 30:
        estimate *= 0.75
        factors.append("viento fuerte")

    return {
        "estimated_visitors": max(0, round(estimate)),
        "score": round(min(100, estimate), 1),
        "confidence": "Baja — falta historial de visitas",
        "factors": factors,
        "is_observed": False,
        "baseline_daily": round(float(baseline_daily or 157), 1),
        "model_version": "climate-v1",
    }
