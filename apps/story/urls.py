from django.urls import path

from . import views

urlpatterns = [
    path("story/", views.latest, name="story"),
    path("older/", views.older, name="older"),
]
