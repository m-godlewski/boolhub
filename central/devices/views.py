from django.http import JsonResponse

from .models import Device


def index(request) -> JsonResponse:
    """Returns list of Room objects"""
    # queries database for list of all Device objects
    query_results = Device.objects.values()
    # converts QuerySet to list
    devices = list(query_results)
    # response dictionary
    response = {
        "data": devices
    }
    return JsonResponse(response)


def device(request, device_id: str) -> JsonResponse:
    """Returns selected Device object."""
    # queries database for list of all Device objects
    query_results = Device.objects.filter(id=device_id).values()
    # converts QuerySet to list
    device = list(query_results)
    # response dictionary
    response = {"data": device}
    return JsonResponse(response)
