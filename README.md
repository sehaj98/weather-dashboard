
# Weather Dashboard 🌦️

A responsive weather dashboard built with Python and Flask.
Search for a city to view current weather conditions and a
five-day forecast.

## Features

- Search weather by city name
- Current temperature and feels-like temperature
- Humidity and wind speed
- Current weather conditions
- Five-day temperature forecast
- Daily chance of precipitation
- Input validation and API error handling
- Automated tests using pytest
- Responsive layout for mobile and desktop

## Tech Stack

- Python
- Flask
- HTML5
- CSS3
- Open-Meteo Geocoding API
- Open-Meteo Weather API
- pytest

## Project Structure

```text
weather-dashboard/
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   └── index.html
├── static/
│   └── style.css
└── tests/
    └── test_app.py
```

## Getting Started

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd weather-dashboard
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your repository URL.

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Run the application

```powershell
python app.py
```

Open this address in your browser:

http://127.0.0.1:5000

## Run Tests

```powershell
python -m pytest -v
```

The tests cover page loading, input validation, successful
weather searches, invalid cities, and API connection errors.

## Weather Data

Weather information is provided by Open-Meteo:

- https://open-meteo.com/

No API key is required for this project's basic API usage.

## Future Improvements

- Weather icons and improved visual design
- Unit conversion between Celsius and Fahrenheit
- Weather forecast charts
- Deployment to a hosting platform
- Continuous integration for automated tests

## License

This project is available for learning and portfolio purposes.
