from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
from apps.achievements import viewsets

router = DefaultRouter()
router.register("achievements", viewsets.AchievementViewSet)


urlpatterns = [
    path("achievements/", views.achievements, name="achievements"),
]
