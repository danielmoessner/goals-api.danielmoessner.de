from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.story import viewsets

from . import views

router = DefaultRouter()
router.register(r"stories", viewsets.StoryViewSet)

urlpatterns = [
    path("story/", views.storyv, name="story"),
]
