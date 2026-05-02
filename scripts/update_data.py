#!/usr/bin/env python3
"""
BD.LIVE Daily Data Updater
Fetches latest weather data and updates the data files.
Called by GitHub Actions on a daily schedule.
"""

import json
import urllib.request
import os
import sys
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(REPO_ROOT, "data")

# Read API key from environment
API_KEY = os.environ.get("OPENWEATHER_API_KEY", "")
if not API_KEY:
    print("ERROR: OPENWEATHER_API_KEY not set")
    sys.exit(1)

CITIES = [
    ("Dhaka", 23.8103, 90.4125),
    ("Chittagong", 22.3569, 91.7832),
    ("Rajshahi", 24.3745, 88.6042),
    ("Khulna", 22.8456, 89.5403),
    ("Barisal", 22.7010, 90.3535),
    ("Sylhet", 24.8949, 91.8687),
    ("Rangpur", 25.7439, 89.2752),
    ("Mymensingh", 24.7471, 90.4203),
    ("Comilla", 23.4607, 91.1809),
    ("Gazipur", 23.9999, 90.4203),
    ("Narayanganj", 23.6238, 90.5000),
    ("Bogra", 24.8465, 89.3773),
    ("Jessore", 23.1667, 89.2167),
    ("Dinajpur", 25.6279, 88.6332),
    ("Brahmanbaria", 23.9608, 91.1115),
    ("Tangail", 24.2513, 89.9167),
    ("Pabna", 24.0064, 89.2372),
    ("Jamalpur", 24.9375, 89.9372),
    ("Naogaon", 24.7936, 88.9318),
    ("Sirajganj", 24.4533, 89.7006),
]


def fetch_weather():
    """Fetch current weather for all cities."""
    results = []
    for name, lat, lon in CITIES:
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=15) as resp:
                d = json.loads(resp.read())
                results.append({
                    "city": name,
                    "lat": lat,
                    "lon": lon,
                    "temp": round(d["main"]["temp"], 1),
                    "feels_like": round(d["main"]["feels_like"], 1),
                    "humidity": d["main"]["humidity"],
                    "wind": round(d["wind"]["speed"], 1),
                    "desc": d["weather"][0]["description"].title(),
                    "icon": d["weather"][0]["icon"],
                    "pressure": d["main"]["pressure"],
                    "visibility": d.get("visibility", 0) / 1000,
                    "updated": d["dt"]
                })
                print(f"  ✓ {name}: {d['main']['temp']}°C, {d['weather'][0]['description']}")
        except Exception as e:
            print(f"  ✗ {name}: {e}", file=sys.stderr)

    return results


def main():
    print(f"BD.LIVE Data Update — {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print(f"Fetching weather for {len(CITIES)} cities...")

    weather = fetch_weather()
    if not weather:
        print("ERROR: No weather data fetched")
        sys.exit(1)

    weather_path = os.path.join(DATA_DIR, "weather.json")
    with open(weather_path, "w") as f:
        json.dump(weather, f, indent=2)

    print(f"\n✓ Saved {len(weather)} cities to data/weather.json")
    print("Update complete!")


if __name__ == "__main__":
    main()
