from rest_framework.routers import DefaultRouter
from apps.achievements import viewsets

router = DefaultRouter()
router.register('achievements', viewsets.AchievementViewSet)
