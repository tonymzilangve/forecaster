import os
import requests
from django.http import HttpResponse
from django.shortcuts import render

from geopy.geocoders import Nominatim


geolocator = Nominatim(user_agent="weather_api")


def fetch_weather_forecast(request, city):

    headers = {
        'X-Yandex-Weather-Key': os.getenv("YANDEX_ACCESS_KEY")
    }
    
    location = geolocator.geocode(city)
    
    response = requests.get(
                        f"{os.getenv('YANDEX_API_URL')}"
                        f"?lat={location.latitude}"
                        f"&lon={location.longitude}",
                        headers=headers)

    weather_now = response.json()["fact"]
    temp = weather_now["temp"]
    pressure = weather_now["pressure_mm"]
    windspeed = weather_now["wind_speed"]
    
    output = {
        "temperature": temp,
        "pressure": pressure,
        "wind speed": windspeed
    }

    return HttpResponse(output)
