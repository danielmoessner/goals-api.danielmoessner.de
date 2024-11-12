from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.goals.models import Goal, Link, ProgressMonitor, Strategy
from apps.goals.serializers import (
    GoalSerializer,
    LinkSerializer,
    MonitorSerializer,
    RecursiveGoalSerializer,
    StrategySerializer,
)


class GoalViewSet(viewsets.ModelViewSet):
    serializer_class = GoalSerializer
    queryset = Goal.objects.none()
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=["get"], detail=False)
    def state(self, request):
        data = {"state": self.request.user.goals.count()}
        return Response(data)

    @action(detail=False, methods=["get"])
    def tree(self, request):
        queryset = Goal.get_goals_user(
            self.request.user,
            "ALL",
            include_archived_goals=self.request.user.show_archived_objects,
        ).prefetch_related("master_goals")
        subgoal_pks = []
        for goal in list(queryset):
            if goal.master_goals.exists():
                subgoal_pks.append(goal.pk)
        queryset = queryset.exclude(pk__in=subgoal_pks)
        serializer = RecursiveGoalSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def get_queryset(self):
        return Goal.get_goals_user(
            self.request.user, "ALL", include_archived_goals=True
        ).prefetch_related("sub_goals")

    def list(self, request, *args, **kwargs):
        queryset = Goal.get_goals_user(
            self.request.user,
            "ALL",
            include_archived_goals=self.request.user.show_archived_objects,
        ).prefetch_related("sub_goals", "strategies", "progress_monitors")
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class StrategyViewSet(viewsets.ModelViewSet):
    serializer_class = StrategySerializer
    queryset = Strategy.objects.none()
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=["get"], detail=False)
    def state(self, request):
        data = {
            "state": Strategy.objects.filter(
                goal__in=self.request.user.goals.all()
            ).count()
        }
        return Response(data)

    def get_queryset(self):
        return Strategy.get_strategies_user(
            self.request.user, include_archived_strategies=True
        )

    def list(self, request, *args, **kwargs):
        queryset = Strategy.get_strategies_user(
            self.request.user,
            include_archived_strategies=self.request.user.show_archived_objects,
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class LinkViewSet(viewsets.ModelViewSet):
    serializer_class = LinkSerializer
    queryset = Link.objects.none()
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=["get"], detail=False)
    def state(self, request):
        data = {
            "state": Link.objects.filter(
                master_goal__in=self.request.user.goals.all()
            ).count()
        }
        return Response(data)

    def get_queryset(self):
        return Link.get_links_user(self.request.user, include_archived_links=True)

    def list(self, request, *args, **kwargs):
        queryset = Link.get_links_user(
            self.request.user,
            include_archived_links=self.request.user.show_archived_objects,
        ).select_related("master_goal", "sub_goal")
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class MonitorViewSet(viewsets.ModelViewSet):
    serializer_class = MonitorSerializer
    queryset = ProgressMonitor.objects.none()
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=["get"], detail=False)
    def state(self, request):
        data = {
            "state": ProgressMonitor.objects.filter(
                goal__in=self.request.user.goals.all()
            ).count()
        }
        return Response(data)

    def get_queryset(self):
        return ProgressMonitor.get_monitors_user(
            self.request.user, included_archived_progress_monitors=True
        )

    def list(self, request, *args, **kwargs):
        queryset = ProgressMonitor.get_monitors_user(
            self.request.user,
            included_archived_progress_monitors=self.request.user.show_archived_objects,
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
