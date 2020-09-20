from apps.users.serializers import UserSerializer
from apps.users.models import CustomUser
from rest_framework import viewsets, permissions


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.none()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CustomUser.objects.filter(pk=self.request.user.pk)
