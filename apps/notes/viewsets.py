from rest_framework import permissions, viewsets

from apps.notes.models import Note
from apps.notes.serializers import NoteListSerializer, NoteSerializer


class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    queryset = Note.objects.none()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return NoteListSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        return self.request.user.notes.all()
