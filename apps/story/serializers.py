from apps.story.models import Story
from rest_framework import serializers


class AddUserMixin:
    def validate(self, attrs):
        attrs = super().validate(attrs)
        if 'user' not in attrs:
            attrs['user'] = self.context['request'].user
        return attrs


class StorySerializer(AddUserMixin, serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Story
        exclude = ['user']
