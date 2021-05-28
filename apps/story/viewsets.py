from rest_framework.response import Response

from apps.story.serializers import StorySerializer
from apps.story.models import Story
from rest_framework import viewsets, permissions, status
from django.utils import timezone


class StoryViewSet(viewsets.ModelViewSet):
    model = Story
    queryset = Story.objects.none()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StorySerializer
    http_method_names = ['get', 'post', 'delete', 'head', 'options', 'trace']

    def get_queryset(self):
        return Story.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        stories = Story.objects.filter(user=request.user, created__date=timezone.now().date())
        if stories.exists():
            serializer = self.get_serializer(stories.first(), data=request.data)
        else:
            serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
