from rest_framework import permissions, viewsets

from apps.achievements.models import Achievement
from apps.achievements.serializers import AchievementSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.none()
    serializer_class = AchievementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Achievement.objects.filter(user=self.request.user)
