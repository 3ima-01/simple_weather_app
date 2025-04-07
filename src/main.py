from fastapi import FastAPI

from weather.router import weather_router
from views.router import views_router

app = FastAPI()

app.include_router(weather_router)
app.include_router(views_router)
