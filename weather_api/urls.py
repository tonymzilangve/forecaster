from django.urls import include, path
from rest_framework import routers
from .views import fetch_weather_forecast, CityViewSet, WeatherRequestView

router = routers.SimpleRouter()
router.register(r"cities", CityViewSet, basename="city")

urlpatterns = [
    path("weather/<str:city>", fetch_weather_forecast),
    path("requests/", WeatherRequestView.as_view()),
    path("", include(router.urls)),
]
