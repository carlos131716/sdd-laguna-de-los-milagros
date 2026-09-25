import requests


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
REQUEST_TIMEOUT = 5


class CityNotFoundError(Exception):
    pass


class WeatherServiceError(Exception):
    pass


class WeatherServiceIncompleteError(WeatherServiceError):
    pass


WEATHER_CODES = {
    0: "Cielo despejado",
    1: "Mayormente despejado",
    2: "Parcialmente nublado",
    3: "Nublado",
    45: "Niebla",
    48: "Niebla con escarcha",
    51: "Llovizna ligera",
    53: "Llovizna moderada",
    55: "Llovizna intensa",
    56: "Llovizna helada ligera",
    57: "Llovizna helada intensa",
    61: "Lluvia ligera",
    63: "Lluvia moderada",
    65: "Lluvia intensa",
    66: "Lluvia helada ligera",
    67: "Lluvia helada intensa",
    71: "Nevada ligera",
    73: "Nevada moderada",
    75: "Nevada intensa",
    77: "Granizo fino",
    80: "Chubascos ligeros",
    81: "Chubascos moderados",
    82: "Chubascos violentos",
    85: "Chubascos de nieve ligeros",
    86: "Chubascos de nieve intensos",
    95: "Tormenta",
    96: "Tormenta con granizo ligero",
    99: "Tormenta con granizo intenso",
}


def get_current_weather(city):
    location = search_city(city)
    current, units = fetch_weather(location["latitude"], location["longitude"])

    try:
        temperature = current["temperature_2m"]
        humidity = current["relative_humidity_2m"]
        wind = current["wind_speed_10m"]
        weather_code = current["weather_code"]
    except KeyError as exc:
        raise WeatherServiceIncompleteError from exc

    return {
        "ciudad": location["name"],
        "pais": location["country"],
        "temperatura": temperature,
        "descripcion": describe_weather(weather_code),
        "humedad": humidity,
        "viento": wind,
        "unidad_viento": units.get("wind_speed_10m", "km/h"),
    }


def search_city(city):
    try:
        response = requests.get(
            GEOCODING_URL,
            params={"name": city, "count": 1, "language": "es", "format": "json"},
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as exc:
        raise WeatherServiceError from exc
    except ValueError as exc:
        raise WeatherServiceIncompleteError from exc

    results = data.get("results") or []
    if not results:
        raise CityNotFoundError

    location = results[0]
    required_fields = ("name", "country", "latitude", "longitude")
    if any(field not in location for field in required_fields):
        raise WeatherServiceIncompleteError

    return location


def fetch_weather(latitude, longitude):
    try:
        response = requests.get(
            FORECAST_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
                "wind_speed_unit": "kmh",
                "timezone": "auto",
            },
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as exc:
        raise WeatherServiceError from exc
    except ValueError as exc:
        raise WeatherServiceIncompleteError from exc

    current = data.get("current")
    units = data.get("current_units", {})
    if not isinstance(current, dict):
        raise WeatherServiceIncompleteError

    return current, units


def describe_weather(code):
    return WEATHER_CODES.get(code, "Condición climática no especificada")
