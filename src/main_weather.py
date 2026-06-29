import sys
from datetime import datetime
from zoneinfo import ZoneInfo

import requests

from config import (
    NOTION_API_KEY,
    NOTION_WEATHER_DATABASE_ID,
    OPENWEATHERMAP_API_KEY,
    OPENWEATHERMAP_CITY,
)
from databases import NotionDatabase


def check_config_variables():
    if OPENWEATHERMAP_API_KEY is None:
        print("Missing API key!")
        sys.exit()

    if NOTION_API_KEY is None:
        print("Missing Database API KEY!")
        sys.exit()

    if NOTION_WEATHER_DATABASE_ID is None:
        print("Missing Database URL!")
        sys.exit()

    print("Start process.")


def get_coord(city: str):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        print(f"Network or API Error: {e}")
        return None


def fetch_24_hour_forecast(lon, lat, api_key):
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={api_key}"

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


# support only 10 countries
def convert_timezone(utc_string: str, target_tz: str) -> str:
    target_tz = target_tz.lower().strip()
    match target_tz:
        case "thailand" | "th":
            simplified_target_tz = "Asia/Bangkok"
        case "united states" | "us" | "usa":
            simplified_target_tz = "America/New_York"
        case "united kingdom" | "uk":
            simplified_target_tz = "Europe/London"
        case "japan" | "jp":
            simplified_target_tz = "Asia/Tokyo"
        case "china" | "cn":
            simplified_target_tz = "Asia/Shanghai"
        case "india" | "in":
            simplified_target_tz = "Asia/Kolkata"
        case "germany" | "de":
            simplified_target_tz = "Europe/Berlin"
        case "france" | "fr":
            simplified_target_tz = "Europe/Paris"
        case "italy" | "it":
            simplified_target_tz = "Europe/Rome"
        case "canada" | "ca":
            simplified_target_tz = "America/Toronto"
        case _:
            simplified_target_tz = "UTC"

    try:
        utc_time = datetime.strptime(utc_string, "%Y-%m-%d %H:%M:%S").replace(
            tzinfo=ZoneInfo("UTC")
        )

        thailand_time = utc_time.astimezone(ZoneInfo(simplified_target_tz))

        return thailand_time.strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        print(f"Error converting time: {e}")
        return utc_string


if __name__ == "__main__":
    check_config_variables()

    # setup notion
    notion = NotionDatabase(
        api_key=NOTION_API_KEY, database_id=NOTION_WEATHER_DATABASE_ID
    )

    fetch_24_hour_forecast(
        lon=get_coord(city=OPENWEATHERMAP_CITY).get("coord").get("lon"),
        lat=get_coord(city=OPENWEATHERMAP_CITY).get("coord").get("lat"),
        api_key=OPENWEATHERMAP_API_KEY,
    )

    # print(fetch_24_hour_forecast(lon=lon, lat=lat, api_key=OPENWEATHERMAP_API_KEY))

    #     forecast_data_24_hour = fetch_24_hour_forecast(
    #
    # return data in forecast_data_24_hour:
    #             properties = {
    #                 "title": {"title": [{"text": {"content": "Weather report"}}]},
    #                 "date": {
    #                     "rich_text": [
    #                         {
    #                             "text": {
    #                                 "content": convert_timezone(
    #                                     utc_string=w.get("date"),
    #                                     target_tz=OPENWEATHERMAP_CITY,
    #                                 )
    #                             }
    #                         }
    #                     ]
    #                 },
    #                 "temp": {"number": float(w.get("temp"))},
    #                 "weather": {"rich_text": [{"text": {"content": w.get("weather")}}]},
    #                 "description": {
    #                     "rich_text": [{"text": {"content": w.get("description")}}]
    #                 },
    #                 "country": {"select": {"name": OPENWEATHERMAP_CITY}},
    #             }

    #             # add to notion database
    #             response = notion.add_row(properties=properties)
    #             print(response)
