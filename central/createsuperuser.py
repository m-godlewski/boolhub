"""
This script initializes superuser base on environmental variables passed in docker-compose file.
"""

import os

from django.db import IntegrityError
from django.contrib.auth.models import User


try:
    superuser = User.objects.create_superuser(
        username=os.environ.get("CENTRAL_USER"),
        password=os.environ.get("CENTRAL_PASSWORD"),
    )
    superuser.save()
except IntegrityError:
    print(f"Super User with username {env('SUPER_USER_NAME')} is already exit!")
except Exception as e:
    print(e)
