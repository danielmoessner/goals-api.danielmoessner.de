from rest_framework.decorators import action
from rest_framework.response import Response
from apps.goals.serializer import GoalSerializer, LinkSerializer, StrategySerializer, MonitorSerializer, \
    RecursiveGoalSerializer
from apps.goals.models import Goal, Strategy, Link, ProgressMonitor
from rest_framework import viewsets, permissions


class GoalViewSet(viewsets.ModelViewSet):
    serializer_class = GoalSerializer
    queryset = Goal.objects.none()
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def starred(self, request):
        queryset = Goal.get_goals_user(
            self.request.user,
            'STAR',
            include_archived_goals=self.request.user.show_archived_objects
        ).prefetch_related(
            'sub_goals'
        )
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def tree(self, request):
        queryset = Goal.get_goals_user(
            self.request.user,
            self.request.user.treeview_goal_choice,
            include_archived_goals=self.request.user.show_archived_objects
        ).prefetch_related('master_goals')
        subgoal_pks = []
        for goal in list(queryset):
            if goal.master_goals.exists():
                subgoal_pks.append(goal.pk)
        queryset = queryset.exclude(pk__in=subgoal_pks)
        serializer = RecursiveGoalSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def main(self, request):
        queryset = Goal.get_goals_user(
            self.request.user,
            self.request.user.goal_view_goal_choice,
            include_archived_goals=self.request.user.show_archived_objects
        ).prefetch_related(
            'sub_goals'
        )
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def subgoals(self, request, pk=None):
        instance = self.get_object()
        sub_goals = Goal.get_goals(
            instance.sub_goals.all(),
            'ALL',
            self.request.user.show_archived_objects
        )
        serializer = self.get_serializer(sub_goals, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def mastergoals(self, request, pk=None):
        instance = self.get_object()
        master_goals = Goal.get_goals(
            instance.master_goals.all(),
            'ALL',
            self.request.user.show_archived_objects
        )
        serializer = self.get_serializer(master_goals, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def strategies(self, request, pk=None):
        instance = self.get_object()
        strategies = instance.strategies.all()
        if not request.user.show_archived_objects:
            strategies = strategies.filter(is_archived=False)
        serializer = StrategySerializer(strategies, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def monitors(self, request, pk=None):
        instance = self.get_object()
        monitors = instance.progress_monitors.all()
        if not request.user.show_archived_objects:
            strategies = monitors.filter(is_archived=False)
        serializer = MonitorSerializer(monitors, many=True, context={'request': request})
        return Response(serializer.data)

    def get_queryset(self):
        return Goal.get_goals_user(
            self.request.user, 'ALL',
            include_archived_goals=True
        ).prefetch_related(
            'sub_goals'
        )

    def list(self, request, *args, **kwargs):
        queryset = Goal.get_goals_user(
            self.request.user, 'ALL',
            include_archived_goals=self.request.user.show_archived_objects
        ).prefetch_related(
            'sub_goals', 'strategies', 'progress_monitors'
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class StrategyViewSet(viewsets.ModelViewSet):
    serializer_class = StrategySerializer
    queryset = Strategy.objects.none()
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def main(self, request):
        queryset = Strategy.get_strategies_user(
            self.request.user,
            self.request.user.strategy_main_choice,
            include_archived_strategies=self.request.user.show_archived_objects
        )
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def starred(self, request):
        queryset = Strategy.get_strategies_user(
            self.request.user,
            'STAR',
            include_archived_strategies=self.request.user.show_archived_objects
        )
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def get_queryset(self):
        return Strategy.get_strategies_user(
            self.request.user, 'ALL',
            include_archived_strategies=True
        )

    def list(self, request, *args, **kwargs):
        queryset = Strategy.get_strategies_user(
            self.request.user, 'ALL',
            include_archived_strategies=self.request.user.show_archived_objects
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class LinkViewSet(viewsets.ModelViewSet):
    serializer_class = LinkSerializer
    queryset = Link.objects.none()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Link.get_links_user(
            self.request.user, 'ALL',
            include_archived_links=True
        )

    def list(self, request, *args, **kwargs):
        queryset = Link.get_links_user(
            self.request.user, 'ALL',
            include_archived_links=self.request.user.show_archived_objects
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class MonitorViewSet(viewsets.ModelViewSet):
    serializer_class = MonitorSerializer
    queryset = ProgressMonitor.objects.none()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ProgressMonitor.get_monitors_user(
            self.request.user, 'ALL',
            included_archived_progress_monitors=True
        )

    def list(self, request, *args, **kwargs):
        queryset = ProgressMonitor.get_monitors_user(
            self.request.user, 'ALL',
            included_archived_progress_monitors=self.request.user.show_archived_objects
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
