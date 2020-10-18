from rest_framework.routers import DefaultRouter
from django.urls import path, include
from apps.notes import viewsets

router = DefaultRouter()
router.register(r'notes', viewsets.NoteViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
