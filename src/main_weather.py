from config import (
    NOTION_API_KEY,
    NOTION_WEATHER_DATABASE_ID,
    OPENWEATHERMAP_API_KEY,
    OPENWEATHERMAP_CITY,
)
from databases import NotionDatabase
from providers import WeatherProvider

# support only 10 countries
# def convert_timezone(utc_string: str, target_tz: str) -> str:
#     target_tz = target_tz.lower().strip()
#     match target_tz:
#         case "thailand" | "th":
#             simplified_target_tz = "Asia/Bangkok"
#         case "united states" | "us" | "usa":
#             simplified_target_tz = "America/New_York"
#         case "united kingdom" | "uk":
#             simplified_target_tz = "Europe/London"
#         case "japan" | "jp":
#             simplified_target_tz = "Asia/Tokyo"
#         case "china" | "cn":
#             simplified_target_tz = "Asia/Shanghai"
#         case "india" | "in":
#             simplified_target_tz = "Asia/Kolkata"
#         case "germany" | "de":
#             simplified_target_tz = "Europe/Berlin"
#         case "france" | "fr":
#             simplified_target_tz = "Europe/Paris"
#         case "italy" | "it":
#             simplified_target_tz = "Europe/Rome"
#         case "canada" | "ca":
#             simplified_target_tz = "America/Toronto"
#         case _:
#             simplified_target_tz = "UTC"

#     try:
#         utc_time = datetime.strptime(utc_string, "%Y-%m-%d %H:%M:%S").replace(
#             tzinfo=ZoneInfo("UTC")
#         )

#         thailand_time = utc_time.astimezone(ZoneInfo(simplified_target_tz))

#         return thailand_time.strftime("%Y-%m-%d %H:%M:%S")
#     except Exception as e:
#         print(f"Error converting time: {e}")
#         return utc_string


if __name__ == "__main__":
    weather_provider = WeatherProvider(
        api_key=OPENWEATHERMAP_API_KEY, city=OPENWEATHERMAP_CITY
    )

    notion = NotionDatabase(
        api_key=NOTION_API_KEY, database_id=NOTION_WEATHER_DATABASE_ID
    )

    reponse_weather = weather_provider.fetch_24_hour_forecast()
    print(reponse_weather)

    # fetch_24_hour_forecast(
    #     lon=get_coord(city=OPENWEATHERMAP_CITY).get("coord").get("lon"),
    #     lat=get_coord(city=OPENWEATHERMAP_CITY).get("coord").get("lat"),
    #     api_key=OPENWEATHERMAP_API_KEY,
    # )

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
