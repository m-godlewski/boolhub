from django.db import models

from rooms.models import Room


class Device(models.Model):
    """Class representation of single device that has access to internet."""

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
        ("console", "Konsola")
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
    # location of device
    location = models.ForeignKey(Room, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        """Returns representation of object in form of string."""
        return f"{self.brand}_{self.name}_{self.location}" if self.location else f"{self.brand}_{self.name}"
