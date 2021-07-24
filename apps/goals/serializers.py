from apps.goals.models import Goal, Strategy, ProgressMonitor, Link
from rest_framework import serializers


class AddUserMixin:
    def validate(self, attrs):
        attrs = super().validate(attrs)
        if 'user' not in attrs:
            attrs['user'] = self.context['request'].user
        return attrs


class GoalSerializer(AddUserMixin, serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='goal-detail')
    id = serializers.ReadOnlyField()

    class Meta:
        model = Goal
        exclude = ['user', 'sub_goals']


class StrategySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='strategy-detail')
    id = serializers.ReadOnlyField()
    goal = serializers.HyperlinkedRelatedField(many=False, view_name='goal-detail', queryset=Goal.objects.none())

    class Meta:
        model = Strategy
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context['request'].user
        self.fields['goal'].queryset = Goal.get_goals_user(user, 'ALL',
                                                           include_archived_goals=user.show_archived_objects)


class MonitorSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='progressmonitor-detail')
    id = serializers.ReadOnlyField()
    goal = serializers.HyperlinkedRelatedField(many=False, view_name='goal-detail', queryset=Goal.objects.none())
    progress = serializers.ReadOnlyField()

    class Meta:
        model = ProgressMonitor
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context['request'].user
        self.fields['goal'].queryset = Goal.get_goals_user(user, 'ALL',
                                                           include_archived_goals=user.show_archived_objects)


class LinkSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='link-detail')
    id = serializers.ReadOnlyField()
    master_goal = serializers.HyperlinkedRelatedField(many=False, view_name='goal-detail',
                                                      queryset=Goal.objects.none())
    sub_goal = serializers.HyperlinkedRelatedField(many=False, view_name='goal-detail',
                                                   queryset=Goal.objects.none())
    mastergoal = GoalSerializer(read_only=True, source='master_goal')
    subgoal = GoalSerializer(read_only=True, source='sub_goal')

    class Meta:
        depth = 1
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
class RecursiveGoalSerializer(AddUserMixin, serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='goal-detail')
    id = serializers.ReadOnlyField()
    subgoals = serializers.SerializerMethodField('get_subgoals')
    monitors = serializers.SerializerMethodField('get_monitors')
    strategies = serializers.SerializerMethodField('get_strategies')

    def get_subgoals(self, goal):
        queryset = goal.get_tree_subgoals(self.context['request'].user)
        serializer = RecursiveGoalSerializer(instance=queryset, many=True, context=self.context)
        return serializer.data

    def get_monitors(self, goal):
        queryset = goal.get_tree_monitors(self.context['request'].user)
        serializer = MonitorSerializer(instance=queryset, many=True, context=self.context)
        return serializer.data

    def get_strategies(self, goal):
        queryset = goal.get_tree_strategies(self.context['request'].user)
        serializer = StrategySerializer(instance=queryset, many=True, context=self.context)
        return serializer.data

    class Meta:
        model = Goal
        exclude = ['user', 'sub_goals']
