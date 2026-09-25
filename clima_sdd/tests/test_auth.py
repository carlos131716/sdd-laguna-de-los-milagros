import tempfile
import os

import pytest

import app as weather_app


@pytest.fixture
def client():
    weather_app.app.config.update(TESTING=True)
    with tempfile.TemporaryDirectory() as directory:
        weather_app.app.config["DATABASE"] = os.path.join(directory, "test.sqlite3")
        with weather_app.app.app_context():
            weather_app.init_db()
        yield weather_app.app.test_client()


def test_anonymous_user_is_redirected_to_login(client):
    response = client.get("/")
    assert response.status_code == 302
    assert "/login" in response.location


def test_register_login_and_logout(client):
    response = client.post("/registro", data={"email": "ana@example.com", "password": "segura123"})
    assert response.status_code == 302
    response = client.post("/login", data={"email": "ana@example.com", "password": "segura123"})
    assert response.status_code == 302
    assert response.location == "/"
    response = client.post("/logout")
    assert response.location == "/login"


def test_duplicate_email_and_short_password_are_rejected(client):
    client.post("/registro", data={"email": "ana@example.com", "password": "segura123"})
    duplicate = client.post("/registro", data={"email": "ANA@example.com", "password": "segura123"})
    short = client.post("/registro", data={"email": "otra@example.com", "password": "123"})
    assert "Ya existe" in duplicate.text
    assert "al menos 8" in short.text


def test_invalid_next_cannot_redirect_outside_site(client):
    response = client.post("/registro", data={"email": "ana@example.com", "password": "segura123"})
    assert response.status_code == 302
    response = client.post("/login?next=https://evil.example", data={"email": "ana@example.com", "password": "segura123"})
    assert response.location == "/"
