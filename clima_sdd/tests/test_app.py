import pytest
import tempfile
import os

import app as weather_app
from weather_service import (
    CityNotFoundError,
    WeatherServiceError,
    WeatherServiceIncompleteError,
)


@pytest.fixture
def client():
    weather_app.app.config.update(TESTING=True)
    with tempfile.TemporaryDirectory() as directory:
        weather_app.app.config["DATABASE"] = os.path.join(directory, "test.sqlite3")
        with weather_app.app.app_context():
            weather_app.init_db()
            db = weather_app.get_db()
            db.execute("INSERT INTO users (email, password_hash) VALUES (?, ?)", ("test@example.com", "scrypt:32768:8:1$test$test"))
            db.commit()
        test_client = weather_app.app.test_client()
        with test_client.session_transaction() as session:
            session["user_id"] = 1
        yield test_client


def test_get_home_shows_form(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Consulta del clima" in response.data
    assert b"name=\"city\"" in response.data


def test_post_valid_city_shows_weather(client, monkeypatch):
    def fake_weather(city):
        assert city == "Tingo Maria"
        return {
            "ciudad": "Tingo Maria",
            "pais": "Peru",
            "temperatura": 28.0,
            "descripcion": "Parcialmente nublado",
            "humedad": 75,
            "viento": 8.0,
            "unidad_viento": "km/h",
        }

    monkeypatch.setattr(weather_app.weather_service, "get_current_weather", fake_weather)

    response = client.post("/", data={"city": "Tingo Maria"})

    assert response.status_code == 200
    assert b"Tingo Maria, Peru" in response.data
    assert b"28.0" in response.data
    assert b"Parcialmente nublado" in response.data
    assert b"75%" in response.data
    assert b"8.0 km/h" in response.data


@pytest.mark.parametrize("city", ["", "   "])
def test_empty_city_does_not_call_service(client, monkeypatch, city):
    def fail_weather(_city):
        raise AssertionError("Weather service should not be called")

    monkeypatch.setattr(weather_app.weather_service, "get_current_weather", fail_weather)

    response = client.post("/", data={"city": city})

    assert response.status_code == 200
    assert b"Ingrese el nombre de una ciudad." in response.data


def test_invalid_city_length_does_not_call_service(client, monkeypatch):
    def fail_weather(_city):
        raise AssertionError("Weather service should not be called")

    monkeypatch.setattr(weather_app.weather_service, "get_current_weather", fail_weather)

    response = client.post("/", data={"city": "A"})

    assert response.status_code == 200
    assert "Ingrese un nombre de ciudad válido." in response.text


def test_city_not_found_message(client, monkeypatch):
    def fake_weather(_city):
        raise CityNotFoundError

    monkeypatch.setattr(weather_app.weather_service, "get_current_weather", fake_weather)

    response = client.post("/", data={"city": "NoExiste"})

    assert b"Ciudad no encontrada." in response.data
    assert b"Temperatura" not in response.data


def test_weather_service_error_message(client, monkeypatch):
    def fake_weather(_city):
        raise WeatherServiceError

    monkeypatch.setattr(weather_app.weather_service, "get_current_weather", fake_weather)

    response = client.post("/", data={"city": "Lima"})

    assert "No se pudo obtener la información del clima." in response.text
    assert b"Temperatura" not in response.data


def test_incomplete_weather_message(client, monkeypatch):
    def fake_weather(_city):
        raise WeatherServiceIncompleteError

    monkeypatch.setattr(weather_app.weather_service, "get_current_weather", fake_weather)

    response = client.post("/", data={"city": "Lima"})

    assert "La información del clima no está disponible en este momento." in response.text
    assert b"Temperatura" not in response.data


def test_second_search_replaces_previous_result(client, monkeypatch):
    results = {
        "Lima": {
            "ciudad": "Lima",
            "pais": "Peru",
            "temperatura": 20,
            "descripcion": "Nublado",
            "humedad": 80,
            "viento": 12,
            "unidad_viento": "km/h",
        },
        "Cusco": {
            "ciudad": "Cusco",
            "pais": "Peru",
            "temperatura": 14,
            "descripcion": "Cielo despejado",
            "humedad": 55,
            "viento": 7,
            "unidad_viento": "km/h",
        },
    }

    monkeypatch.setattr(weather_app.weather_service, "get_current_weather", lambda city: results[city])

    first = client.post("/", data={"city": "Lima"})
    second = client.post("/", data={"city": "Cusco"})

    assert b"Lima, Peru" in first.data
    assert b"Cusco, Peru" in second.data
    assert b"Lima, Peru" not in second.data
