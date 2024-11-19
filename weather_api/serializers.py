from rest_framework import serializers
from .models import City, WeatherRequest


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


class WeatherRequestSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)

    class Meta:
        model = WeatherRequest
        fields = "__all__"
