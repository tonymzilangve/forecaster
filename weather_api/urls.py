from django.urls import include, path
from rest_framework import routers
from .views import CityViewSet, WeatherAPIView, WeatherRequestView

router = routers.SimpleRouter()
router.register(r"cities", CityViewSet, basename="city")

urlpatterns = [
    path("weather/<str:city>", WeatherAPIView.as_view(), name="weather_info"),
    path("requests/", WeatherRequestView.as_view(), name="weather_requests"),
    path("", include(router.urls)),
]
