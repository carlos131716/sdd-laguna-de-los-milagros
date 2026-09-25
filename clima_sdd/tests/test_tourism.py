import os
import tempfile

import pytest

import app as weather_app
from backend.tourism import get_place, predict_visitors


@pytest.fixture
def client():
    weather_app.app.config.update(TESTING=True)
    with tempfile.TemporaryDirectory() as directory:
        weather_app.app.config["DATABASE"] = os.path.join(directory, "tourism.sqlite3")
        with weather_app.app.app_context():
            weather_app.init_db()
            db = weather_app.get_db()
            db.execute("INSERT INTO users (email, password_hash) VALUES (?, ?)", ("tourism@example.com", "scrypt:32768:8:1$test$test"))
            db.commit()
        test_client = weather_app.app.test_client()
        with test_client.session_transaction() as session:
            session["user_id"] = 1
        yield test_client


def test_laguna_de_los_milagros_is_the_initial_place():
    place = get_place("laguna-de-los-milagros")
    assert place["name"] == "Laguna de los Milagros"
    assert place["region"] == "Huánuco"
    official = place["official_2024"]
    assert official["foreign"] + official["national"] + official["local"] == 57465


def test_prediction_is_explainable_and_not_observed():
    prediction = predict_visitors({
        "temperature_2m": 25,
        "relative_humidity_2m": 70,
        "wind_speed_10m": 8,
        "weather_code": 1,
    })
    assert prediction["estimated_visitors"] > 0
    assert prediction["is_observed"] is False
    assert prediction["confidence"].startswith("Baja")
    assert prediction["factors"]


def test_tourism_index_is_available_to_authenticated_user(client):
    response = client.get("/turismo")
    assert response.status_code == 200
    assert b"Laguna de los Milagros" in response.data


def test_tourism_detail_shows_calibrated_estimate(client, monkeypatch):
    monkeypatch.setattr(
        weather_app.weather_service,
        "fetch_weather",
        lambda *_args: ({
            "temperature_2m": 25,
            "relative_humidity_2m": 70,
            "wind_speed_10m": 8,
            "weather_code": 1,
        }, {"wind_speed_10m": "km/h"}),
    )
    response = client.get("/turismo/laguna-de-los-milagros")
    assert response.status_code == 200
    assert b"57,465" in response.data
    assert b"visitantes estimados hoy" in response.data
