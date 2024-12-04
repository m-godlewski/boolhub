from django.http.response import Http404
from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Settings
from .serializers import SettingsSerializer


class SettingsView(APIView):

    def get(self, request, pk=1):
        """Returns one and only instance of Settings model from database."""
        try:
            data = Settings.objects.get(id=pk)
            serializer = SettingsSerializer(data)
        except Settings.DoesNotExist:
            raise Http404(
                "Settings has not been initialized during installation process!"
            )
        return Response(serializer.data)

    def put(self, request, pk=1):
        """Updates one and only instance of Settings model."""
        settings_to_update = Settings.objects.get(id=pk)
        serializer = SettingsSerializer(
            instance=settings_to_update, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return JsonResponse("Settings updated", safe=False)
        return JsonResponse("Failed to update settings")
