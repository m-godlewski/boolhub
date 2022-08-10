from django.shortcuts import render


def index(request):
    """Rendering landing page of central application."""
    return render(request, "index.html")
