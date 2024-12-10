from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
from apps.goals import viewsets

router = DefaultRouter()
router.register(r"goals", viewsets.GoalViewSet)
router.register(r"strategies", viewsets.StrategyViewSet)
router.register(r"monitors", viewsets.MonitorViewSet)
router.register(r"links", viewsets.LinkViewSet)

urlpatterns = [
    path("goals/", views.goals, name="goals"),
    path("goal/<int:pk>/", views.goal, name="goal"),
]
