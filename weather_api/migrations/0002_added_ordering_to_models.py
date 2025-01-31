# Generated by Django 5.1.3 on 2024-11-19 13:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("weather_api", "0001_created_weather_request_model"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="city",
            options={
                "ordering": ("name",),
                "verbose_name": "City",
                "verbose_name_plural": "Cities",
            },
        ),
        migrations.AlterModelOptions(
            name="weatherrequest",
            options={
                "ordering": ("-timestamp",),
                "verbose_name": "Weather request",
                "verbose_name_plural": "Weather requests",
            },
        ),
    ]
