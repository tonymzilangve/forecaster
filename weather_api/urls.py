from django.urls import path
from .views import fetch_weather_forecast

urlpatterns = [
    path("weather/<str:city>", fetch_weather_forecast)
]
