from django.urls import path

from . import views


# url patterns of devices app
urlpatterns = [
    path("", view=views.index),
]
