from django.forms.models import model_to_dict
from weather_api.models import City, WeatherRequest
from tests.base import TestViewBase, TestViewSetBase, merge


class TestWeatherRequestsView(TestViewBase):
    basename = "weather_requests"
    weather_request: WeatherRequest
    city: City
    wr_attributes: dict 
    city_attributes = {
        "name": "Samara",
        "latitude": "13,918675",
        "longitude": "-11.876330"
    }

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.city = City.objects.create(**cls.city_attributes)
        cls.wr_attributes = {
            "city": cls.city,
            "temperature": -10,
            "pressure": 766,
            "wind_speed": 12.3,
            "source_type": "web",
        }

    @staticmethod
    def expected_details(entity: dict, attributes: dict) -> dict:
        return {**attributes, "id": entity["id"], "city": entity["city"]}

    def create_weather_request(self, data: dict = None) -> dict:
        attributes = merge(self.wr_attributes, data)
        return model_to_dict(WeatherRequest.objects.create(**attributes))        
    
    def test_create(self) -> None:
        weather_request = self.create_weather_request()
        
        expected_response = self.expected_details(weather_request, self.wr_attributes)
        assert weather_request == expected_response

    def test_list(self) -> None:
        wr1 = self.create_weather_request({
            "temperature": -11.5,
            "timestamp": "2024-11-25T12:00:00Z"
        })
        wr2 = self.create_weather_request({
            "temperature": -8.5,
            "timestamp": "2024-11-25T12:00:00Z"
        })
        wr3 = self.create_weather_request({
            "temperature": -5.5,
            "timestamp": "2024-11-26T12:00:00Z"
        })

        self.assert_list_ids(expected=[wr3, wr2, wr1])

    def test_ordering(self) -> None:
        wr1 = self.create_weather_request({
            "temperature": -11.5,
            "timestamp": "2024-11-24T12:00:00Z"
        })
        wr2 = self.create_weather_request({
            "temperature": -8.5,
            "timestamp": "2024-11-25T12:00:00Z"
        })
        wr3 = self.create_weather_request({
            "temperature": -5.5,
            "timestamp": "2024-11-26T12:00:00Z"
        })

        self.assert_list_ids(expected=[wr1, wr2, wr3], query={"ordering": "timestamp"})

    def test_filter_source_type(self) -> None:
        wr1 = self.create_weather_request()
        wr2 = self.create_weather_request({"source_type": "telegram"})

        self.assert_list_ids(expected=[wr2], query={"source_type": "telegram"})
