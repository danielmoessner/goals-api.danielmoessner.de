from django.urls import path

from . import views

urlpatterns = [
    path("goals/", views.goals, name="goals"),
    path("goal/<int:pk>/", views.goal, name="goal"),
]
