from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Room
from .serializer import RoomSerializer
from devices.models import Device
from devices.serializer import DeviceSerializer


@api_view(["GET"])
def rooms(request) -> Response:
    """Returns list of all Room object."""
    query_result = Room.objects.all()
    serializer = RoomSerializer(query_result, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def room(request, room_id: str) -> Response:
    """Returns selected Room object."""
    query_result = Room.objects.get(pk=room_id)
    serializer = RoomSerializer(query_result)
    return Response(serializer.data)


@api_view(["GET"])
def room_devices(request, room_id: str) -> Response:
    """Returns list of Device objects assigned to selected Room object."""
    query_results = Device.objects.filter(location_id=room_id)
    serializer = DeviceSerializer(query_results, many=True)
    return Response(serializer.data)
