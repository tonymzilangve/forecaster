import os
import requests
from django.http import Http404, HttpResponse
from rest_framework import generics

from geopy.geocoders import Nominatim
from .models import City, WeatherRequest
from .serializers import WeatherRequestSerializer


geolocator = Nominatim(user_agent="weather_api")


def fetch_weather_forecast(request, city):

    headers = {
        'X-Yandex-Weather-Key': os.getenv("YANDEX_ACCESS_KEY")
    }
    
    city_info = City.objects.filter(name=city.capitalize()).first()
    
    if not city_info:
        location = geolocator.geocode(city)
        if not location:
            raise Http404
        
        lat = location.latitude
        lon = location.longitude
        city_info = City.objects.create(name=city.capitalize(), latitude=lat, longitude=lon)
    else:
        lat = city_info.latitude
        lon = city_info.longitude
    
    response = requests.get(
                        f"{os.getenv('YANDEX_API_URL')}"
                        f"?lat={lat}"
                        f"&lon={lon}",
                        headers=headers)

    weather_now = response.json()["fact"]
    temp = weather_now["temp"]
    pressure = weather_now["pressure_mm"]
    windspeed = weather_now["wind_speed"]
    
    new_request = WeatherRequest.objects.create(
        city=city_info,
        temperature=temp,
        pressure=pressure,
        wind_speed=windspeed
    )
    
    output = {
        "temperature": temp,
        "pressure": pressure,
        "wind speed": windspeed
    }

    return HttpResponse(output)


class WeatherRequestView(generics.ListAPIView):
    queryset = WeatherRequest.objects.all()
    serializer_class = WeatherRequestSerializer
