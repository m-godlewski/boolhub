from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    """Devices lighting page view."""
    return render(
        request=request,
        template_name="lighting.html"
    )
