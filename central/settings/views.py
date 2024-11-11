from django.http import JsonResponse

from .models import Settings


def index(request) -> JsonResponse:
    """Returns current settings values."""
    # queries database for settings object
    query_results = Settings.objects.filter(id=1).values()
    # converts QuerySet to dictionary
    settings = list(query_results)[0]
    # response dictionary
    response = {
        "data": {
            "temperature": {
                "min": settings.get("temperature_min"),
                "max": settings.get("temperature_max"),
                "notify": settings.get("notify_temperature"),
            },
            "humidity": {
                "min": settings.get("humidity_min"),
                "max": settings.get("humidity_max"),
                "notify": settings.get("notify_humidity"),
            },
            "aqi": {
                "threshold": settings.get("aqi_threshold"),
                "notify": settings.get("notify_aqi"),
            },
            "network": {
                "overload_threshold": settings.get(
                    "network_overload_threshold"
                ),
                "notify_overload": settings.get("notify_network_overload"),
                "notify_unknown_device": settings.get("notify_unknown_device"),
            },
            "health": {
                "threshold": settings.get("health_threshold"),
                "notify": settings.get("notify_health"),
            },
            "weather": {
                "url": settings.get("weather_api_url"),
                "latitude": settings.get("weather_api_latitude"),
                "longitude": settings.get("weather_api_longitude"),
            },
        }
    }
    return JsonResponse(response)
