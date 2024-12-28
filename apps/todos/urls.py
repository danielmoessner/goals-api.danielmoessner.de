from django.shortcuts import render
from django.urls import path

from ..todos import views

urlpatterns = [
    path("todos/", views.todos, name="todos"),
    path("wuerfel/", lambda r: render(r, "wuerfel.html")),
]
