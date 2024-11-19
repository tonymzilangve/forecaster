from django.urls import path
from .views import fetch_weather_forecast, WeatherRequestView

urlpatterns = [
    path("weather/<str:city>", fetch_weather_forecast),
    path("requests/", WeatherRequestView.as_view())
]
