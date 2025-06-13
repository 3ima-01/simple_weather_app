from fastapi import APIRouter

from config import settings
from open_weather import open_weather_client

weather_router = APIRouter(tags=["Weather"], prefix="/weather")


@weather_router.get("/{city}")
async def get_weather_by_city(city: str):
    city = city.lower()
    key = "weather_" + city
    if settings.rd.get(key):
        return settings.rd.get(key)
    else:
        data = open_weather_client.get_current_weather_data(city)
        settings.rd.set(key, data, ex=60)
        return data


@weather_router.get("/forecast/{city}")
async def get_weather_forecast_by_city(city: str):
    city = city.lower()
    key = "forecast_" + city
    if settings.rd.get(key):
        return settings.rd.get(key)
    else:
        data = open_weather_client.get_five_days_forecast(city)
        settings.rd.set(key, data, ex=60)
    return data


@weather_router.get("/air_pollution/{city}")
async def get_air_pollution_by_city(city: str):
    city = city.lower()
    key = "air_pollution_" + city
    if settings.rd.get(key):
        return settings.rd.get(key)
    else:
        data = open_weather_client.get_air_pollution(city)
        settings.rd.set(key, data, ex=60)
    return data
