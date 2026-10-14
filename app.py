
import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from flask import Flask, render_template, request

app = Flask(__name__)

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Rain showers",
    81: "Moderate rain showers",
    82: "Heavy rain showers",
    85: "Snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with hail",
    99: "Thunderstorm with heavy hail",
}


def fetch_json(url, params):
    """Fetch JSON from a URL with a timeout."""
    full_url = f"{url}?{urlencode(params)}"
    req = Request(
        full_url,
        headers={"User-Agent": "WeatherDashboard/1.0"},
    )

    with urlopen(req, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def get_weather(city):
    """Get current conditions and a five-day forecast."""

    location_data = fetch_json(
        "https://geocoding-api.open-meteo.com/v1/search",
        {
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json",
        },
    )

    locations = location_data.get("results", [])

    if not locations:
        return None, [], "City not found. Check the spelling and try again."

    location = locations[0]

    weather_data = fetch_json(
        "https://api.open-meteo.com/v1/forecast",
        {
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "current": (
                "temperature_2m,relative_humidity_2m,"
                "apparent_temperature,weather_code,wind_speed_10m"
            ),
            "daily": (
                "weather_code,temperature_2m_max,"
                "temperature_2m_min,precipitation_probability_max"
            ),
            "forecast_days": 5,
            "timezone": "auto",
        },
    )

    current = weather_data.get("current")
    daily = weather_data.get("daily")

    if not current or not daily:
        return None, [], "Weather data is currently unavailable."

    weather_code = current.get("weather_code")

    weather = {
        "city": location["name"],
        "region": location.get("admin1", ""),
        "country": location.get("country", ""),
        "temperature": current.get("temperature_2m"),
        "feels_like": current.get("apparent_temperature"),
        "humidity": current.get("relative_humidity_2m"),
        "wind_speed": current.get("wind_speed_10m"),
        "condition": WEATHER_CODES.get(
            weather_code, "Unknown conditions"
        ),
        "time": current.get("time", ""),
        "temperature_unit": weather_data.get(
            "current_units", {}
        ).get("temperature_2m", "°C"),
        "wind_unit": weather_data.get(
            "current_units", {}
        ).get("wind_speed_10m", "km/h"),
    }

    forecast = []
    daily_units = weather_data.get("daily_units", {})

    dates = daily.get("time", [])
    codes = daily.get("weather_code", [])
    highs = daily.get("temperature_2m_max", [])
    lows = daily.get("temperature_2m_min", [])
    rain_chances = daily.get("precipitation_probability_max", [])

    for i, date in enumerate(dates):
        forecast.append({
            "date": date,
            "condition": WEATHER_CODES.get(
                codes[i], "Unknown conditions"
            ),
            "high": highs[i],
            "low": lows[i],
            "rain": rain_chances[i] if i < len(rain_chances) else None,
            "temperature_unit": daily_units.get(
                "temperature_2m_max", "°C"
            ),
        })

    return weather, forecast, ""


@app.route("/", methods=["GET", "POST"])
def home():
    city = ""
    message = ""
    weather = None
    forecast = []

    if request.method == "POST":
        city = request.form.get("city", "").strip()

        if not city:
            message = "Please enter a city name."
        elif len(city) > 80:
            message = "City name must be 80 characters or fewer."
        else:
            try:
                weather, forecast, message = get_weather(city)
            except (HTTPError, URLError, TimeoutError):
                message = (
                    "Could not connect to the weather service. "
                    "Check your internet and try again."
                )
            except (ValueError, KeyError, TypeError, IndexError):
                message = (
                    "Unexpected weather data received. "
                    "Please try again later."
                )

    return render_template(
        "index.html",
        city=city,
        message=message,
        weather=weather,
        forecast=forecast,
    )


if __name__ == "__main__":
    app.run(debug=True)
