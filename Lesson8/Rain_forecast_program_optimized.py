import requests
import json
import os
from datetime import datetime, timedelta


class WeatherForecast:
    def __init__(self, latitude, longitude, cache_file="weather_cache.json"):
        self.latitude = latitude
        self.longitude = longitude
        self.cache_file = cache_file
        self._data = self._load()

    def _load(self):
        if os.path.exists(self.cache_file):
            with open(self.cache_file, "r") as f:
                return json.load(f)
        return {}

    def _save(self):
        with open(self.cache_file, "w") as f:
            json.dump(self._data, f, indent=4)

    def _fetch(self, date):
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={self.latitude}&longitude={self.longitude}"
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

    # Interpret result
    def _interpret(self, value):
        if value is None or value < 0:
            return "I don't know"
        elif value == 0.0:
            return "It will not rain"
        else:
            return f"It will rain (precipitation: {value} mm)"

    #  Set item
    def __setitem__(self, date, value):
        self._data[date] = value
        self._save()

    #  Get item
    def __getitem__(self, date):
        # Return cached if exists
        if date in self._data:
            return self._data[date]

        # Otherwise fetch, store, and return
        precipitation = self._fetch(date)
        result = self._interpret(precipitation)

        self._data[date] = result
        self._save()

        return result

    # Iterator (iterate over dates)
    def __iter__(self):
        return iter(self._data)

    #  Items generator
    def items(self):
        for date, weather in self._data.items():
            yield (date, weather)



def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def get_next_day():
    return (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")



def main():
    wf = WeatherForecast(latitude=50.1109, longitude=8.6821)

    user_input = input("Enter date (YYYY-mm-dd) or press Enter for tomorrow: ").strip()

    if user_input == "":
        date = get_next_day()
    else:
        if not validate_date(user_input):
            print("Invalid date format.")
            return
        date = user_input

    # using __getitem__
    result = wf[date]

    print(f"\nDate: {date}")
    print(result)

    print("\nSaved dates:")
    for d in wf:
        print(d)

    print("\nSaved forecasts:")
    for d, weather in wf.items():
        print(f"{d}: {weather}")


if __name__ == "__main__":
    main()