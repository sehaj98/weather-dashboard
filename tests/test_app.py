
import pytest

import app as weather_app


@pytest.fixture
def client():
    weather_app.app.config["TESTING"] = True

    with weather_app.app.test_client() as test_client:
        yield test_client


def test_home_page_loads(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Weather Dashboard" in response.data


def test_empty_city_is_rejected(client):
    response = client.post("/", data={"city": ""})

    assert response.status_code == 200
    assert b"Please enter a city name." in response.data


def test_city_name_over_80_characters_is_rejected(client):
    response = client.post("/", data={"city": "A" * 81})

    assert response.status_code == 200
    assert b"80 characters or fewer" in response.data


def test_invalid_city_shows_message(client, monkeypatch):
    def fake_get_weather(city):
        return None, [], "City not found. Check the spelling and try again."

    monkeypatch.setattr(weather_app, "get_weather", fake_get_weather)

    response = client.post("/", data={"city": "XYZABC123"})

    assert response.status_code == 200
    assert b"City not found" in response.data


def test_successful_search_displays_weather(client, monkeypatch):
    sample_weather = {
        "city": "Amritsar",
        "region": "Punjab",
        "country": "India",
        "temperature": 30.0,
        "feels_like": 32.0,
        "humidity": 60,
        "wind_speed": 10.0,
        "condition": "Mainly clear",
        "time": "2026-10-14T12:00",
        "temperature_unit": "°C",
        "wind_unit": "km/h",
    }

    sample_forecast = [
        {
            "date": "2026-10-14",
            "condition": "Clear sky",
            "high": 32.0,
            "low": 23.0,
            "rain": 10,
            "temperature_unit": "°C",
        }
    ]

    def fake_get_weather(city):
        return sample_weather, sample_forecast, ""

    monkeypatch.setattr(weather_app, "get_weather", fake_get_weather)

    response = client.post("/", data={"city": "Amritsar"})

    assert response.status_code == 200
    assert b"Amritsar" in response.data
    assert b"30.0" in response.data
    assert b"5-day forecast" in response.data
    assert b"Clear sky" in response.data


def test_api_connection_error_is_handled(client, monkeypatch):
    def fake_get_weather(city):
        raise weather_app.URLError("Connection failed")

    monkeypatch.setattr(weather_app, "get_weather", fake_get_weather)

    response = client.post("/", data={"city": "Amritsar"})

    assert response.status_code == 200
    assert b"Could not connect to the weather service" in response.data
