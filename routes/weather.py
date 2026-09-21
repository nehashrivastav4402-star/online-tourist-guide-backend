from flask import Blueprint, jsonify, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

weather = Blueprint("weather", __name__)

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")


@weather.route("/weather", methods=["GET"])
def get_weather():

    city = request.args.get("city")

    if not city:
        return jsonify({
            "message": "City is required"
        }), 400

    if not OPENWEATHER_API_KEY:
        return jsonify({
            "message": "OpenWeather API key is not configured"
        }), 500

    try:
        url = "https://api.openweathermap.org/data/2.5/weather"

        params = {
            "q": city,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric"
        }

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        data = response.json()

        if response.status_code != 200:
            return jsonify({
                "message": data.get(
                    "message",
                    "Unable to fetch weather"
                )
            }), response.status_code

        weather_data = {
            "city": data.get("name"),
            "country": data.get("sys", {}).get("country"),
            "temperature": data.get("main", {}).get("temp"),
            "feels_like": data.get("main", {}).get("feels_like"),
            "humidity": data.get("main", {}).get("humidity"),
            "pressure": data.get("main", {}).get("pressure"),
            "wind_speed": data.get("wind", {}).get("speed"),
            "condition": data.get(
                "weather", [{}]
            )[0].get(
                "description",
                "No description"
            ),
            "weather_main": data.get(
                "weather", [{}]
            )[0].get(
                "main",
                "Unknown"
            ),
            "icon": data.get(
                "weather", [{}]
            )[0].get(
                "icon",
                ""
            )
        }

        return jsonify(weather_data), 200

    except requests.exceptions.Timeout:
        return jsonify({
            "message": "Weather service timed out"
        }), 504

    except requests.exceptions.RequestException:
        return jsonify({
            "message": "Unable to connect to weather service"
        }), 500

    except Exception as e:
        return jsonify({
            "message": "Something went wrong",
            "error": str(e)
        }), 500