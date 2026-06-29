import requests


class WeatherProvider:
    def __init__(self, api_key, city):
        if not api_key:
            raise ConnectionError("Youtube Provider: Require api key")

        self.api_key = api_key
        self.city = city

        print(self.api_key)
        print(self.city)

        print("Weather provider init.")

    def get_coord(self):
        url = f"https://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.api_key}&units=metric"

        try:
            response = requests.get(url)
            data = response.json()

            if response.status_code != 200:
                print(f"API Error {response.status_code}: {data.get('message', 'Unknown error')}")
                return None

            return data.get("coord")

        except requests.exceptions.RequestException as e:
            print(f"Network or API Error: {e}")
            return None

    def fetch_24_hour_forecast(self):
        coord = self.get_coord()

        if not coord:
            print("Could not retrieve coordinates.")
            return None

        lon = coord.get("lon")
        lat = coord.get("lat")

        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={self.api_key}"

        try:
            response = requests.get(url)
            data = response.json()
            next_24_hours = data["list"][:8]

            simplified_forecast = []
            for item in next_24_hours:
                forecast_point = {
                    "date": item["dt_txt"],
                    "temp": item["main"]["temp"],
                    "weather": item["weather"][0]["main"],
                    "description": item["weather"][0]["description"],
                }
                simplified_forecast.append(forecast_point)
            return simplified_forecast

        except Exception as e:
            print(f"Error fetching the 24-hour forecast: {e}")
