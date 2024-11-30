from django.db import models


class Settings(models.Model):
    """Class representation of system settings."""

    # temperature
    temperature_min = models.IntegerField(default=19)
    temperature_max = models.IntegerField(default=27)
    notify_temperature = models.BooleanField(default=True)

    # humidity
    humidity_min = models.IntegerField(default=20)
    humidity_max = models.IntegerField(default=85)
    notify_humidity = models.BooleanField(default=True)

    # aqi
    aqi_threshold = models.IntegerField(default=50)
    notify_aqi = models.BooleanField(default=True)

    # network
    network_overload_threshold = models.IntegerField(default=10)
    notify_network_overload = models.BooleanField(default=True)
    notify_unknown_device = models.BooleanField(default=True)

    # devices health
    health_threshold = models.IntegerField(default=15)
    notify_health = models.BooleanField(default=True)

    # weather
    weather_api_url = models.CharField(max_length=250, blank=True, null=True)
    weather_api_latitude = models.CharField(max_length=250, blank=True, null=True)
    weather_api_longitude = models.CharField(max_length=250, blank=True, null=True)
    weather_api_token = models.CharField(max_length=250, blank=True, null=True)

    def save(self, *args, **kwargs):
        """Override save method to avoid existence of many servings models."""
        if not self.pk and Settings.objects.exists():
            raise Exception("There can be only one Setting object in database.")
        return super(Settings, self).save(*args, **kwargs)

    class Meta:
        db_table = "settings"