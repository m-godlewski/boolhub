from django.db import models


class Device(models.Model):
    """"""

    name = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    mac_address = models.CharField(max_length=17)

    def __str__(self) -> str:
        """Returns representation of object in form of string."""
        return self.name
