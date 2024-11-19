from rest_framework import serializers
from .models import City, WeatherRequest


class WeatherRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherRequest
        fields = "__all__"


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"
