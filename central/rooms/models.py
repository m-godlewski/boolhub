from django.db import models


class Room(models.Model):
    """Class representation of single room."""

    # room name
    name = models.CharField(max_length=30)
    # room dimensions
    length = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()

    def __str__(self) -> str:
        """Returns representation of object in form of string."""
        return self.name.capitalize()
