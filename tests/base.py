import copy 
from http import HTTPStatus
from typing import List, Union

from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework.response import Response



def merge(base: dict, another_values: dict = None) -> dict:
        result = copy.deepcopy(base)
        if another_values:
                result.update(another_values)
        return result


class TestViewBase(APITestCase):
    client: APIClient = None
    
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.client = APIClient()

    @classmethod
    def list_url(cls, args: List[Union[str, int]] = None) -> str:
        return reverse(f"{cls.basename}", args=args)

    @classmethod
    def _assert_pagination(cls, response_json: dict) -> None:
        results = response_json["results"]
        assert response_json == {
            "count": len(results),
            "next": None,
            "previous": None,
            "results": results,
        }

    @classmethod
    def _assert_no_pagination(cls, response_json: dict) -> None:
        assert list(response_json.keys()) == ["results"]

    def list(self, data: dict = None, args: List[Union[str, int]] = None, pagination: bool = True) -> dict:
        response = self.client.get(self.list_url(args), data=data)
        assert response.status_code == HTTPStatus.OK, response.content
        
        if pagination:
            self._assert_pagination(response.json())
        else:
            self._assert_no_pagination(response.json())
        
        return response.data 
    
    @classmethod
    def ids(cls, items: List[dict]) -> List[int]:
        return [item["id"] for item in items]

    def assert_list_ids(
        self,
        expected: List[dict],
        query: dict = None,
        args: Union[str, int] = None
    ) -> None:
        entities = self.list(query, args)["results"]
        assert self.ids(entities) == self.ids(expected)


class TestViewSetBase(APITestCase):
    client: APIClient = None
    
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.client = APIClient()

    @classmethod
    def detail_url(cls, args: Union[str, int]) -> str:
        if isinstance(args, list):
            return reverse(f"{cls.basename}-detail", args=args)
        else:
            return reverse(f"{cls.basename}-detail", args=[args])

    @classmethod
    def list_url(cls, args: List[Union[str, int]] = None) -> str:
        return reverse(f"{cls.basename}-list", args=args)

    def request_create(self, data: dict, args: List[Union[str, int]] = None) -> Response:
        return self.client.post(self.list_url(args), data=data)        

    def create(self, data: dict, args: List[Union[str, int]] = None) -> dict:
        response = self.client.post(self.list_url(args), data=data)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.data

    @classmethod
    def _assert_pagination(cls, response_json: dict) -> None:
        results = response_json["results"]
        assert response_json == {
            "count": len(results),
            "next": None,
            "previous": None,
            "results": results,
        }

    @classmethod
    def _assert_no_pagination(cls, response_json: dict) -> None:
        assert list(response_json.keys()) == ["results"]

    def list(self, data: dict = None, args: List[Union[str, int]] = None, pagination: bool = True) -> dict:
        response = self.client.get(self.list_url(args), data=data)
        assert response.status_code == HTTPStatus.OK, response.content
        
        if pagination:
            self._assert_pagination(response.json())
        else:
            self._assert_no_pagination(response.json())
        
        return response.data

    def request_retrieve(self, args: Union[str, int]) -> Response:
        return self.client.get(self.detail_url(args))

    def retrieve(self, args: Union[str, int]) -> dict:
        response = self.request_retrieve(args)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def update(self, args: Union[str, int], data: dict) -> dict:
        response = self.client.put(self.detail_url(args), data=data)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def partial_update(self, args: Union[str, int], data: dict) -> dict:
        response = self.client.patch(self.detail_url(args), data=data)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def delete(self, args: Union[int, list] = None) -> dict:
        response = self.client.delete(self.detail_url(args))
        assert response.status_code == HTTPStatus.NO_CONTENT
        return response.data   
    
    @classmethod
    def ids(cls, items: List[dict]) -> List[int]:
        return [item["id"] for item in items]

    def assert_list_ids(
        self,
        expected: List[dict],
        query: dict = None,
        args: Union[str, int] = None
    ) -> None:
        entities = self.list(query, args)["results"]
        assert self.ids(entities) == self.ids(expected)
