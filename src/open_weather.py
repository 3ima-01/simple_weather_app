from httpx import get

from config import settings
from exceptions import InvalidToken


class OpenWeatherClient:
    def __init__(self):
        self.URL = settings.OPEN_WEATHER_BASE_URL
        self.API_KEY = settings.OPEN_WEATHER_API_KEY

    def get_geo_by_city(self, city: str) -> list:
        key = "geo_" + city

        if settings.rd.get(key):
            return settings.rd.get(key).split(",")
        else:
            r = get(
                f"{self.URL}/geo/1.0/direct",
                params={
                    "q": city,
                    "limit": 1,
                    "appid": self.API_KEY,
                },
            )

            if r.status_code == 401:
                raise InvalidToken

            data = r.json()[0]
            settings.rd.set(key, f"{data['lat']},{data['lon']}")
            return [data["lat"], data["lon"]]

    def get_current_weather_data(
        self,
        city: str,
        units: str = "metric",
        lang: str = "ru",
    ) -> dict:
        lat, lon = self.get_geo_by_city(city)
        r = get(
            f"{self.URL}/data/2.5/weather",
            params={
                "lat": lat,
                "lon": lon,
                "appid": self.API_KEY,
                "units": units,
                "lang": lang,
            },
        )

        if r.status_code == 401:
            raise InvalidToken

        return r.text

    def get_five_days_forecast(
        self,
        city: str,
        units: str = "metric",
        lang: str = "ru",
    ) -> dict:
        lat, lon = self.get_geo_by_city(city)
        r = get(
            f"{self.URL}/data/2.5/forecast",
            params={
                "lat": lat,
                "lon": lon,
                "appid": self.API_KEY,
                "units": units,
                "lang": lang,
            },
        )

        if r.status_code == 401:
            raise InvalidToken

        return r.text

    def get_air_pollution(
        self,
        city: str,
    ) -> dict:
        lat, lon = self.get_geo_by_city(city)
        r = get(
            f"{self.URL}/data/2.5/air_pollution",
            params={
                "lat": lat,
                "lon": lon,
                "appid": self.API_KEY,
            },
        )

        if r.status_code == 401:
            raise InvalidToken

        return r.text


open_weather_client = OpenWeatherClient()
