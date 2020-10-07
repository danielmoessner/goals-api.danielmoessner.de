from apps.goals.models import Goal, Strategy, ProgressMonitor, Link
from rest_framework import serializers


class AddUserMixin:
    def validate(self, attrs):
        attrs = super().validate(attrs)
        if 'user' not in attrs:
            attrs['user'] = self.context['request'].user
        return attrs


class GoalSerializer(AddUserMixin, serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='goals:goal-detail')
    sub_goals = serializers.HyperlinkedRelatedField(many=True, view_name='goals:goal-detail', read_only=True)
    id = serializers.ReadOnlyField()

    class Meta:
        model = Goal
        exclude = ['user']


class StrategySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='goals:strategy-detail')
    id = serializers.ReadOnlyField()
    goal = serializers.HyperlinkedRelatedField(many=False, view_name='goals:goal-detail', read_only=True)

    class Meta:
        model = Strategy
        exclude = []


class MonitorSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='goals:progressmonitor-detail')
    id = serializers.ReadOnlyField()
    goal = serializers.HyperlinkedRelatedField(many=False, view_name='goals:goal-detail', read_only=True)

    class Meta:
        model = ProgressMonitor
        exclude = []


class LinkSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='goals:link-detail')
    id = serializers.ReadOnlyField()
    master_goal = serializers.HyperlinkedRelatedField(many=False, view_name='goals:goal-detail', read_only=True)
    sub_goal = serializers.HyperlinkedRelatedField(many=False, view_name='goals:goal-detail', read_only=True)

    class Meta:
        model = Link
        exclude = []
