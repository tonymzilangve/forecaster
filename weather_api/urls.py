from django.urls import path
from .views import fetch_weather_forecast

urlpatterns = [
    path("weather/", fetch_weather_forecast)
]
