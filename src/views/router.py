import json
from datetime import datetime
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from open_weather import open_weather_client
from config import settings


views_router = APIRouter(tags=["Views"], prefix="/views")
templates = Jinja2Templates(directory="templates")


def datetime_from_unix(value):
    return datetime.fromtimestamp(value).strftime("%Y-%m-%d")


templates.env.filters["datetime"] = datetime_from_unix


@views_router.get("/weather/{city}")
async def get_weather_by_city(request: Request, city: str):
    city = city.lower()
    key = "weather_" + city
    if settings.rd.get(key):
        data = settings.rd.get(key)
    else:
        data = open_weather_client.get_current_weather_data(city)
        settings.rd.set(key, data, ex=60)

    return templates.TemplateResponse(
        request=request,
        name="weather.html",
        context={
            "data": json.loads(data),
        },
    )


@views_router.get("/weather/forecast/{city}")
async def get_weather_forecast_by_city(request: Request, city: str):
    city = city.lower()
    key = "forecast_" + city
    if settings.rd.get(key):
        data = settings.rd.get(key)
    else:
        data = open_weather_client.get_five_days_forecast(city)
        settings.rd.set(key, data, ex=60)

    return templates.TemplateResponse(
        request=request,
        name="forecast.html",
        context={
            "data": json.loads(data),
        },
    )


@views_router.get("/weather/air_pollution/{city}")
def get_air_pollution_by_city(request: Request, city: str):
    city = city.lower()
    key = "air_pollution_" + city
    if settings.rd.get(key):
        data = settings.rd.get(key)
    else:
        data = open_weather_client.get_air_pollution(city)
        settings.rd.set(key, data, ex=60)

    return templates.TemplateResponse(
        request=request,
        name="air_pollution.html",
        context={
            "data": json.loads(data),
        },
    )
