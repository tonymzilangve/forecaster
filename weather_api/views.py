import os
import requests

from django.http import HttpResponse, request
from django.shortcuts import render


def fetch_weather_forecast(request):

    headers = {
        'X-Yandex-Weather-Key': os.getenv("YANDEX_ACCESS_KEY")
    }

    response = requests.get(f'{os.getenv("YANDEX_API_URL")}', headers=headers)

    return HttpResponse(response)
