from rest_framework.routers import DefaultRouter
from apps.notes import viewsets

router = DefaultRouter()
router.register(r'notes', viewsets.NoteViewSet)
