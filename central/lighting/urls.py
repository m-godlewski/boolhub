from django.urls import path

from . import views


# url patterns of v app
urlpatterns = [path("", view=views.index, name="lighting_index")]
