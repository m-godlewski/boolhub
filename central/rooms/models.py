from django.db import models


class Room(models.Model):
    """Class representation of single room."""

    # room name
    name = models.CharField(max_length=30)
    # room dimensions
    length = models.FloatField(null=True)
    width = models.FloatField(null=True)
    height = models.FloatField(null=True)

    def __str__(self) -> str:
        """Returns representation of object in form of string."""
        return self.name.capitalize()
