from rest_framework.routers import DefaultRouter
from apps.notes import viewsets
from django.urls import path
from . import views


router = DefaultRouter()
router.register(r'notes', viewsets.NoteViewSet)

urlpatterns = [
    path("notes/", views.notes, name="notes"),
]