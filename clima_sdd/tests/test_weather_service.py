import requests

import weather_service
from weather_service import (
    CityNotFoundError,
    WeatherServiceError,
    WeatherServiceIncompleteError,
)


class FakeResponse:
    def __init__(self, payload=None, status_error=None, json_error=None):
        self.payload = payload or {}
        self.status_error = status_error
        self.json_error = json_error

    def raise_for_status(self):
        if self.status_error:
            raise self.status_error

    def json(self):
        if self.json_error:
            raise self.json_error
        return self.payload


def test_get_current_weather_returns_internal_model(monkeypatch):
    responses = [
        FakeResponse(
            {
                "results": [
                    {
                        "name": "Tingo Maria",
                        "country": "Peru",
                        "latitude": -9.29,
                        "longitude": -75.99,
                    }
                ]
            }
        ),
        FakeResponse(
            {
                "current": {
                    "temperature_2m": 28.0,
                    "relative_humidity_2m": 75,
                    "weather_code": 2,
                    "wind_speed_10m": 8.0,
                },
                "current_units": {"wind_speed_10m": "km/h"},
            }
        ),
    ]

    def fake_get(*_args, **_kwargs):
        return responses.pop(0)

    monkeypatch.setattr(weather_service.requests, "get", fake_get)

    result = weather_service.get_current_weather("Tingo Maria")

    assert result == {
        "ciudad": "Tingo Maria",
        "pais": "Peru",
        "temperatura": 28.0,
        "descripcion": "Parcialmente nublado",
        "humedad": 75,
        "viento": 8.0,
        "unidad_viento": "km/h",
    }


def test_search_city_raises_city_not_found(monkeypatch):
    monkeypatch.setattr(
        weather_service.requests,
        "get",
        lambda *_args, **_kwargs: FakeResponse({"results": []}),
    )

    try:
        weather_service.search_city("NoExiste")
    except CityNotFoundError:
        assert True
    else:
        assert False, "Expected CityNotFoundError"


def test_search_city_network_error(monkeypatch):
    def fake_get(*_args, **_kwargs):
        raise requests.Timeout

    monkeypatch.setattr(weather_service.requests, "get", fake_get)

    try:
        weather_service.search_city("Lima")
    except WeatherServiceError:
        assert True
    else:
        assert False, "Expected WeatherServiceError"


def test_fetch_weather_missing_current_object(monkeypatch):
    monkeypatch.setattr(
        weather_service.requests,
        "get",
        lambda *_args, **_kwargs: FakeResponse({"current_units": {}}),
    )

    try:
        weather_service.fetch_weather(-12.0, -77.0)
    except WeatherServiceIncompleteError:
        assert True
    else:
        assert False, "Expected WeatherServiceIncompleteError"


def test_get_current_weather_incomplete_current_data(monkeypatch):
    monkeypatch.setattr(
        weather_service,
        "search_city",
        lambda _city: {
            "name": "Lima",
            "country": "Peru",
            "latitude": -12.0,
            "longitude": -77.0,
        },
    )
    monkeypatch.setattr(weather_service, "fetch_weather", lambda *_args: ({}, {}))

    try:
        weather_service.get_current_weather("Lima")
    except WeatherServiceIncompleteError:
        assert True
    else:
        assert False, "Expected WeatherServiceIncompleteError"


def test_describe_unknown_weather_code():
    assert weather_service.describe_weather(999) == "Condición climática no especificada"
