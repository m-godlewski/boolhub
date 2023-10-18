from django.shortcuts import render


def index(request):
    """Rendering landing page of central application."""
    return render(request, "index.html")


def network(request):
    """Rendering network overview page."""
    return render(request, "network.html")


def air(request):
    """Rendering air overview page."""
    return render(request, "air.html")
