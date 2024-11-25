import os
import requests

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from geopy.geocoders import Nominatim
from .models import City, WeatherRequest
from .serializers import CitySerializer, WeatherRequestSerializer
from .utils import YANDEX_HEADERS


geolocator = Nominatim(user_agent="weather_api")


class WeatherAPIView(APIView):
    def get(self, request, city):
        city_info = City.objects.filter(name=city.capitalize()).first()
        
        if not city_info:
            location = geolocator.geocode(city)
            if not location:
                return Response({"error_msg": f"City with name {city} does not exist!"})
            
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
                            headers=YANDEX_HEADERS)

        source = request.query_params.get("source_type", "web")
        
        weather_now = response.json()["fact"]
        temp = weather_now["temp"]
        pressure = weather_now["pressure_mm"]
        windspeed = weather_now["wind_speed"]
        
        new_request = WeatherRequest.objects.create(
            city=city_info,
            temperature=temp,
            pressure=pressure,
            wind_speed=windspeed,
            source_type=source,
        )
        
        output = {
            "temperature": temp,
            "pressure": pressure,
            "wind_speed": windspeed,
        }

        return Response({city: output})


class WeatherRequestView(generics.ListAPIView):
    queryset = WeatherRequest.objects.all()
    serializer_class = WeatherRequestSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["source_type"]
    ordering_fields = ["city", "timestamp"]
    ordering = ["city", "-timestamp"]


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
