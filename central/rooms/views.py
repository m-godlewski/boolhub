from django.http import JsonResponse

from .models import Room
from devices.models import Device


def index(request) -> JsonResponse:
    """Returns list of Room objects."""
    # queries database for list of all Room objects
    query_results = Room.objects.all().values()
    # converts QuerySet to list
    rooms = list(query_results)
    # response dictionary
    response = {"data": rooms}
    return JsonResponse(response)


def room(request, room_id: str) -> JsonResponse:
    """Returns selected Room object."""
    # queries database for list of all Device objects
    query_results = Room.objects.filter(id=room_id).values()
    # converts QuerySet to list
    room = list(query_results)
    # response dictionary
    response = {"data": room}
    return JsonResponse(response)


def room_devices(request, room_id: str) -> JsonResponse:
    """Returns list of Device objects assigned to selected Room object."""
    # queries database for list of all Device objects
    query_results = Device.objects.filter(location_id=room_id).values()
    # converts QuerySet to list
    room_devices = list(query_results)
    # response dictionary
    response = {"data": room_devices}
    return JsonResponse(response)
