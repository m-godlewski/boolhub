from django.urls import path

from . import views


# url patterns of lighting app
urlpatterns = [
    path("", view=views.index, name="lighting_index"),
    path("room/<str:room_id>", view=views.toggle_room, name="lighting_room"),
    path("device/<str:device_id>", view=views.toggle_device, name="lighting_device")
]
