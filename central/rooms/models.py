from django.db import models


class House(models.Model):
    """Class representation of house.
    There should be only one object of this house in system.
    All instances of Room class should be related to one House instance.
    """

    # house dimensions
    length = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()

    def __str__(self) -> str:
        """Returns representation of object in form of string."""
        return "Mieszkanie"


class Room(models.Model):
    """Class representation of single room."""

    # room name
    name = models.CharField(max_length=30)
    # room location
    location = models.ForeignKey(House, default=1, on_delete=models.CASCADE)
    # room dimensions
    length = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()

    def __str__(self) -> str:
        """Returns representation of object in form of string."""
        return self.name.capitalize()
