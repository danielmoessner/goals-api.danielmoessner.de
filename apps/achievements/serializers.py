from apps.achievements.models import Achievement
from rest_framework import serializers


class AchievementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Achievement
        fields = '__all__'
