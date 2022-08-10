from django.db import models

from rooms.models import Room


class Device(models.Model):
    """"""

    name = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    mac_address = models.CharField(max_length=17)
    location = models.ForeignKey(Room, null=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        """Returns representation of object in form of string."""
        return self.name
