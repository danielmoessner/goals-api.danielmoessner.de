from apps.achievements.serializers import AchievementSerializer
from apps.achievements.models import Achievement
from rest_framework import viewsets, permissions


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.none()
    serializer_class = AchievementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Achievement.objects.filter(user=self.request.user)
