import requests
from datetime import datetime, timedelta
import json
import os

CACHE_FILE = "weather_cache.json"


def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}


def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=4)


def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def get_next_day():
    return (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")


def fetch_weather(latitude, longitude, date):
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}"
        f"&daily=precipitation_sum"
        f"&timezone=Europe%2FLondon"
        f"&start_date={date}&end_date={date}"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        return data.get("daily", {}).get("precipitation_sum", [None])[0]

    except requests.RequestException:
        return None


def interpret_result(value):
    if value is None or value < 0:
        return "I don't know"
    elif value == 0.0:
        return "It will not rain"
    else:
        return f"It will rain (precipitation: {value} mm)"


def main():
    latitude = 50.1109
    longitude = 8.6821

    user_input = input("Enter date (YYYY-mm-dd) or press Enter for tomorrow: ").strip()

    if user_input == "":
        date = get_next_day()
    else:
        if not validate_date(user_input):
            print("Invalid date format. Please use YYYY-mm-dd.")
            return
        date = user_input

    cache = load_cache()

    if date in cache:
        print("Result loaded from cache.")
        result = cache[date]
    else:
        precipitation = fetch_weather(latitude, longitude, date)
        result = interpret_result(precipitation)

        cache[date] = result
        save_cache(cache)

    print(f"Date: {date}")
    print(result)


if __name__ == "__main__":
    main()