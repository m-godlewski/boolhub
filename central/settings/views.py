from django.http.response import Http404
from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Settings
from .serializers import SettingsSerializer


class SettingsView(APIView):
    """Class responsible for CRUD operation on Settings object."""

    def get(self, request) -> JsonResponse:
        """Returns one and only instance of Settings model from database."""
        try:
            # database query
            query_result = Settings.objects.get(id=1)
            # serialization
            serializer = SettingsSerializer(query_result)
        except Settings.DoesNotExist:
            raise Http404(
                "Settings has not been initialized during installation process!"
            )
        return Response(serializer.data)

    def put(self, request) -> JsonResponse:
        """Updates one and only instance of Settings model."""
        # database query
        query_result = Settings.objects.get(id=1)
        # serialization
        serializer = SettingsSerializer(
            instance=query_result, data=request.data, partial=True
        )
        # validation
        if serializer.is_valid():
            serializer.save()
            return JsonResponse("Settings updated", safe=False)
        return JsonResponse("Failed to update settings")
