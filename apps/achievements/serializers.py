from rest_framework import serializers

from apps.achievements.models import Achievement


class AddUserMixin:
    def validate(self, attrs):
        attrs = super().validate(attrs)
        if "user" not in attrs:
            attrs["user"] = self.context["request"].user
        return attrs


class AchievementSerializer(AddUserMixin, serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Achievement
        exclude = ["user"]
