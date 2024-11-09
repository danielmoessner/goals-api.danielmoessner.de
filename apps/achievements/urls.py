from rest_framework.routers import DefaultRouter
from apps.achievements import viewsets
from django.urls import path
from . import views

router = DefaultRouter()
router.register('achievements', viewsets.AchievementViewSet)


urlpatterns = [
    path("achievements/", views.achievements, name="achievements"),
]