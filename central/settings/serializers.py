from rest_framework import serializers

from .models import Settings


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = (
            "temperature_min",
            "temperature_max",
            "notify_temperature",
            "humidity_min",
            "humidity_max",
            "notify_humidity",
            "aqi_threshold",
            "notify_aqi",
            "network_overload_threshold",
            "notify_network_overload",
            "notify_unknown_device",
            "health_threshold",
            "notify_health",
            "weather_api_url",
            "weather_api_latitude",
            "weather_api_longitude",
        )
