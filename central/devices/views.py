from django.http import HttpResponse


def index(request):
    """Devices landing page view."""
    return HttpResponse("Index page of devices app!")
