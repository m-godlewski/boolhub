from django.urls import path

from . import views


# url patterns of lighting app
urlpatterns = [
    path("", view=views.index),
]
