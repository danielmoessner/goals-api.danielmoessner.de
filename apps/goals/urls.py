from rest_framework.routers import DefaultRouter
from django.urls import path, include
from apps.goals import viewsets

router = DefaultRouter()
router.register(r'goals', viewsets.GoalViewSet)
router.register(r'strategies', viewsets.StrategyViewSet)
router.register(r'monitors', viewsets.MonitorViewSet)
router.register(r'links', viewsets.LinkViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
