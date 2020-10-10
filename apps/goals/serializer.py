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
    goal = serializers.HyperlinkedRelatedField(many=False, view_name='goals:goal-detail', queryset=Goal.objects.none())

    class Meta:
        model = Strategy
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context['request'].user
        self.fields['goal'].queryset = Goal.get_goals_user(user, 'ALL',
                                                           include_archived_goals=user.show_archived_objects)


class MonitorSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='goals:progressmonitor-detail')
    id = serializers.ReadOnlyField()
    goal = serializers.HyperlinkedRelatedField(many=False, view_name='goals:goal-detail', queryset=Goal.objects.none())

    class Meta:
        model = ProgressMonitor
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context['request'].user
        self.fields['goal'].queryset = Goal.get_goals_user(user, 'ALL',
                                                           include_archived_goals=user.show_archived_objects)


class LinkSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='goals:link-detail')
    id = serializers.ReadOnlyField()
    master_goal = serializers.HyperlinkedRelatedField(many=False, view_name='goals:goal-detail',
                                                      queryset=Goal.objects.none())
    sub_goal = serializers.HyperlinkedRelatedField(many=False, view_name='goals:goal-detail',
                                                   queryset=Goal.objects.none())

    class Meta:
        model = Link
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context['request'].user
        queryset = Goal.get_goals_user(user, 'ALL', include_archived_goals=user.show_archived_objects)
        self.fields['master_goal'].queryset = queryset
        self.fields['sub_goal'].queryset = queryset


###
# Tree
###
class RecursiveGoalSerializer(GoalSerializer):
    def get_fields(self):
        fields = super().get_fields()
        fields['sub_goals'] = RecursiveGoalSerializer(many=True, context=self.context)
        fields['strategies'] = StrategySerializer(many=True, context=self.context)
        fields['progress_monitors'] = MonitorSerializer(many=True, context=self.context)
        return fields
