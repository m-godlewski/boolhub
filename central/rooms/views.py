from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Room
from .serializer import RoomSerializer


@api_view(["GET"])
def rooms(request) -> Response:
    """Returns list of all Room object."""
    query_result = Room.objects.all()
    serializer = RoomSerializer(query_result, many=True)
    return Response(serializer.data)
