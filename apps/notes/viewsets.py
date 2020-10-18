from rest_framework import viewsets
from apps.notes.models import Note
from apps.notes.serializers import NoteSerializer


class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    queryset = Note.objects.none()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.notes.all()
