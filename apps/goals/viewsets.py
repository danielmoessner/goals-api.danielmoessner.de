from datetime import timezone

from rest_framework.decorators import action
from rest_framework.response import Response
from apps.goals.serializer import GoalSerializer, LinkSerializer, StrategySerializer, MonitorSerializer
from apps.goals.models import Goal, Strategy, Link, ProgressMonitor

from rest_framework import viewsets, permissions


class GoalViewSet(viewsets.ModelViewSet):
    serializer_class = GoalSerializer
    queryset = Goal.objects.none()
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def main(self, request):
        queryset = Goal.get_goals_user(
            self.request.user,
            self.request.user.goal_view_goal_choice,
            include_archived_goals=self.request.user.show_archived_objects
        )
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def get_queryset(self):
        return Goal.get_goals_user(
            self.request.user, 'ALL',
            include_archived_goals=True
        )

    def list(self, request, *args, **kwargs):
        queryset = Goal.get_goals_user(
            self.request.user, 'ALL',
            include_archived_goals=self.request.user.show_archived_objects
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
