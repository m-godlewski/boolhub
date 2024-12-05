from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Device
from .serializer import DeviceSerializer


@api_view(["GET"])
def devices(request) -> Response:
    """Returns list of Room objects"""
    query_result = Device.objects.all()
    serializer = DeviceSerializer(query_result, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def device(request, device_id: str) -> Response:
    """Returns selected Device object."""
    query_result = Device.objects.get(pk=device_id)
    serializer = DeviceSerializer(query_result)
    return Response(serializer.data)
