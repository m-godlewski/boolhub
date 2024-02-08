from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from yeelight import Bulb

from devices.models import Device
from rooms.models import Room


def index(request):
    """Renders main panel of lighting module."""
    # query database for each room object
    query_results = Room.objects.all()
    # packs room object in context dictionary
    context = {room.name: room for room in query_results}
    # renders template
    return render(request=request, template_name="lighting.html", context=context)


def toggle_room(request, room_id: int):
    """."""
    pass


def toggle_device(request, device_id: int) -> None:
    """Toggle power of lighting device with given id."""

    # TODO currently only supports yeelight bulb

    # retrieves selected device object
    device = Device.objects.get(id=device_id)
    # creates Bulb object
    bulb = Bulb(device.ip_address)
    # toggling power
    bulb.toggle()
    # redirects back to main lighting panel
    return redirect("/lighting")
