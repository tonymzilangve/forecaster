from weather_api.models import City
from tests.base import TestViewSetBase, merge


class TestCityViewSet(TestViewSetBase):
    basename = "city"
    city: City
    city_attributes = {
        "name": "Samara",
        "latitude": "13,918675",
        "longitude": "-11.876330"
    }
    
    @staticmethod
    def expected_details(entity: dict, attributes: dict) -> dict:
        return {**attributes, "id": entity["id"]}

    def create_city(self, data: dict = None) -> dict:
        attributes = merge(self.city_attributes, data)
        return self.create(attributes)
    
    def test_create(self) -> None:
        city = self.create_city()
        
        expected_response = self.expected_details(city, self.city_attributes)
        assert city == expected_response

    def test_list(self) -> None:
        city1 = self.create_city({"name": "Berlin"})
        city2 = self.create_city({"name": "Manila"})
        city3 = self.create_city({"name": "Milan"})

        self.assert_list_ids(expected=[city1, city2, city3])

    def test_retrieve(self) -> None:
        city1 = self.create_city({"name": "Paris"})
        self.create_city({"name": "Rome"})
        
        response = self.retrieve(city1["id"])

        assert response == city1

    def test_update(self) -> None:
        city = self.create_city({"name": "New York"})
        
        updated_city = self.update(city["id"], self.city_attributes)
        
        expected_result = self.expected_details(city, self.city_attributes)
        assert updated_city == expected_result

    def test_partial_update(self) -> None:
        city = self.create_city({"name": "Machester"})

        updated_city = self.partial_update(city["id"], self.city_attributes)

        expected_result = self.expected_details(city, self.city_attributes)
        assert updated_city == expected_result

    def test_delete(self) -> None:
        city1 = self.create_city()
        city2 = self.create_city({"name": "Istanbul"})

        self.delete(city1["id"])
        
        self.assert_list_ids(expected=[city2])
