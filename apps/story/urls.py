from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
from apps.story import viewsets

router = DefaultRouter()
router.register(r"stories", viewsets.StoryViewSet)

urlpatterns = [
    path("story/", views.latest, name="story"),
    path("older/", views.older, name="older"),
]
