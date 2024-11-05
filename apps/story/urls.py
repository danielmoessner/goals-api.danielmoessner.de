from rest_framework.routers import DefaultRouter
from apps.story import viewsets

router = DefaultRouter()
router.register(r'stories', viewsets.StoryViewSet)
