"""
This script initializes superuser base on environmental variables passed in docker-compose file.
"""

import os

from django.db import IntegrityError
from django.contrib.auth.models import User
from settings.models import Settings


# create superuser model
try:
    superuser = User.objects.create_superuser(
        username=os.environ.get("CENTRAL_USER"),
        password=os.environ.get("CENTRAL_PASSWORD"),
    )
    superuser.save()
except IntegrityError:
    print(f"Super User with username {os.environ.get('CENTRAL_USER')} is already exit!")
except Exception as e:
    print(e)


# create superuser initial settings
try:
    superuser_settings = Settings(
        id=1,
        temperature_min=19.0,
        temperature_max=27.0,
        notify_temperature=True,
        humidity_min=20,
        humidity_max=85,
        notify_humidity=True,
        aqi_threshold=50,
        notify_aqi=True,
        network_overload_threshold=10,
        notify_network_overload=True,
        notify_unknown_device=True,
        health_threshold=15,
        notify_health=True,
        weather_api_url="",
        weather_api_latitude="",
        weather_api_longitude="",
        weather_api_token=""
    )
    superuser_settings.save()
except Exception as e:
    print(e)
