from django.http import JsonResponse

from rooms.models import Room


def index(request):
    """Returns list of Room objects"""
    # queries database for list of all Room objects
    query_results = Room.objects.values()
    # converts QuerySet to list
    rooms = list(query_results)
    # response dictionary
    response = {
        "data": rooms
    }
    return JsonResponse(response)
