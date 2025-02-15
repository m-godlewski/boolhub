from django.db import models

from rooms.models import Room


class Device(models.Model):
    """Class representation of single device in local network."""

    # list of available device categories
    DEVICE_CATEGORY = [
        ("network", "Urządzenie sieciowe"),
        ("computer", "PC/Laptop"),
        ("smartphone", "Smartfon/Komórka"),
        ("tablet", "Tablet/Czytnik"),
        ("printer", "Drukarka"),
        ("tv", "TV/Odtwarzacz multimedialny"),
        ("light", "Oświetlenie"),
        ("air", "Oczyszczacz powietrza/termometr"),
        ("console", "Konsola"),
        ("other", "Inne"),
    ]

    # device name
    name = models.CharField(max_length=50)
    # type of device
    category = models.CharField(max_length=50, choices=DEVICE_CATEGORY)
    # producer of device
    brand = models.CharField(max_length=50)
    # MAC address of physical device
    mac_address = models.CharField(max_length=17)
    # IPv4 address of physical device
    ip_address = models.CharField(max_length=15, null=True, blank=True)
    # authorization token
    token = models.CharField(max_length=64, null=True, blank=True)
    # location of device
    location = models.ForeignKey(Room, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        """Returns representation of object in form of string."""
        return (
            f"{self.brand} {self.name} [{self.location}]"
            if self.location
            else f"{self.brand} {self.name}"
        )
