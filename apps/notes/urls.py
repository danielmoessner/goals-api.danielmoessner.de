from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
from apps.notes import viewsets

router = DefaultRouter()
router.register(r"notes", viewsets.NoteViewSet)

urlpatterns = [
    path("notes/", views.notes, name="notes"),
]
