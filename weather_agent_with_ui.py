# app.py

from flask import Flask, render_template_string, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "http://api.weatherapi.com/v1/current.json"

#  UI HTML
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Weather App UI</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    body { height: 100vh; background: linear-gradient(to bottom right, #cbaaff, #ffd6fa); display: flex; align-items: center; justify-content: center; overflow: hidden; flex-direction: column; gap: 20px; }
    .input-container { display: flex; gap: 10px; justify-content: center; }
    .input-container input { padding: 10px 14px; border-radius: 12px; border: 1px solid #ccc; font-size: 16px; width: 200px; }
    .input-container button { padding: 10px 18px; border: none; background-color: #7b2ff7; color: white; border-radius: 12px; font-size: 16px; cursor: pointer; }
    .weather-card { background: #ffffff; width: 350px; border-radius: 24px; box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2); padding: 20px 24px; display: flex; flex-direction: column; gap: 20px; }
    .header { display: flex; justify-content: space-between; align-items: center; }
    .location { font-size: 20px; font-weight: bold; }
    .weather-icon img { width: 50px; }
    .temp { font-size: 64px; font-weight: bold; text-align: center; }
    .condition { font-size: 20px; color: #555; text-align: center; }
    .forecast { display: flex; justify-content: space-between; gap: 10px; }
    .day { background: #f4f4f4; padding: 10px; border-radius: 12px; flex: 1; text-align: center; }
    .day span { display: block; font-size: 12px; color: #777; }
    .metrics { display: flex; justify-content: space-between; flex-wrap: wrap; gap: 10px; }
    .metric { background: #f4f4f4; padding: 10px; border-radius: 12px; flex: 1 1 45%; text-align: center; }
    .metric-title { font-size: 12px; color: #777; }
    .metric-value { font-size: 16px; font-weight: bold; }
  </style>
</head>
<body>
  <form class="input-container" method="POST">
    <input type="text" name="city" id="cityInput" placeholder="Enter city name" required />
    <button type="submit">Search</button>
  </form>

  <div class="weather-card">
    <div class="header">
      <div class="location" id="cityName">{{ weather.city }}</div>
      <div class="weather-icon">
        <img src="{{ weather.icon }}" alt="weather icon" />
      </div>
    </div>

    <div class="temp">{{ weather.temp }}</div>
    <div class="condition">{{ weather.condition }}</div>

    <div class="forecast">
      <div class="day">Mon <span>28°C</span></div>
      <div class="day">Tue <span>30°C</span></div>
      <div class="day">Wed <span>26°C</span></div>
      <div class="day">Thu <span>29°C</span></div>
    </div>

    <div class="metrics">
      <div class="metric"><div class="metric-title">Golden Hour</div><div class="metric-value">5:38 PM</div></div>
      <div class="metric"><div class="metric-title">UV Index</div><div class="metric-value">5</div></div>
      <div class="metric"><div class="metric-title">Air Quality</div><div class="metric-value">Moderate</div></div>
      <div class="metric"><div class="metric-title">Humidity</div><div class="metric-value">{{ weather.humidity }}%</div></div>
    </div>
  </div>
</body>
</html>
"""

def fetch_weather(city):
    params = {"key": WEATHER_API_KEY, "q": city}
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    
    if response.status_code != 200 or "error" in data:
        return {
            "city": "Not Found",
            "temp": "N/A",
            "condition": "Invalid city",
            "icon": "https://cdn-icons-png.flaticon.com/512/1146/1146869.png",
            "humidity": "N/A"
        }

    return {
        "city": data["location"]["name"],
        "temp": f"{data['current']['temp_c']}°C",
        "condition": data["current"]["condition"]["text"],
        "icon": f"https:{data['current']['condition']['icon']}",
        "humidity": data["current"]["humidity"]
    }

@app.route("/", methods=["GET", "POST"])
def index():
    city = "Lahore"
    if request.method == "POST":
        city = request.form.get("city", "Lahore")
    weather = fetch_weather(city)
    return render_template_string(HTML_TEMPLATE, weather=weather)

if __name__ == "__main__":
    app.run(debug=True)
