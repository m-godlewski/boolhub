from django.urls import path

from . import views


# url patterns of devices app
urlpatterns = [
    path("", view=views.devices),
    path("<str:device_id>", view=views.device),
]
