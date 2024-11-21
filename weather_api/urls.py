from django.urls import include, path
from rest_framework import routers
from .views import CityViewSet, WeatherAPIView, WeatherRequestView

router = routers.SimpleRouter()
router.register(r"cities", CityViewSet, basename="city")

urlpatterns = [
    path("weather/<str:city>", WeatherAPIView.as_view()),
    path("requests/", WeatherRequestView.as_view()),
    path("", include(router.urls)),
]
