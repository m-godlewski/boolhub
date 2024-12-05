from rest_framework import serializers

from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    """Class used for serialization of Room model."""

    class Meta:
        model = Room
        fields = (
            "name",
            "length",
            "width",
            "height",
        )
