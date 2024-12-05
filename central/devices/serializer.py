from rest_framework import serializers

from .models import Device


class DeviceSerializer(serializers.ModelSerializer):
    """Class used for serialization of Device model."""

    class Meta:
        model = Device
        fields = (
            "name",
            "category",
            "brand",
            "mac_address",
            "ip_address",
            "token",
            "location",
        )
