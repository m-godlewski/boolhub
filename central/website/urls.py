from django.urls import path

from . import views


# url patterns of devices app
urlpatterns = [
    path("", view=views.index, name="index"),
    path("network", view=views.network, name="network"),
    path("air", view=views.air, name="air")
]
