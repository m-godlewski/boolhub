from django.urls import path

from . import views


# url patterns of rooms app
urlpatterns = [
    path("", view=views.rooms),
    path("air", view=views.rooms_air),
]
