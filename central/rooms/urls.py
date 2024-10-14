from django.urls import path

from . import views


# url patterns of lighting app
urlpatterns = [
    path("", view=views.index),
    path("<str:room_id>", view=views.room),
    path("<str:room_id>/devices", view=views.room_devices)
]
