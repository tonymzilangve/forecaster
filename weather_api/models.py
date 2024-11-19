from django.db import models


class City(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False, verbose_name='City')
    latitude = models.CharField(max_length=200)
    longitude = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'


class WeatherRequest(models.Model):
    class SourceTypes(models.TextChoices):
        WEB = "web", "Web"
        TG = "telegram", "Telegram"
    
    city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="weather")
    temperature = models.FloatField()
    pressure = models.FloatField()
    wind_speed = models.FloatField()
    source_type = models.CharField(choices=SourceTypes.choices, default=SourceTypes.WEB)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Weather in {self.city} on {self.timestamp}"
    
    class Meta:
        verbose_name = 'Weather request'
        verbose_name_plural = 'Weather requests'
