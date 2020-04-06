from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.db.models import Q

from mastergoal.goals.models import NeverEndingToDo
from mastergoal.goals.models import ProgressMonitor
from mastergoal.goals.models import RepetitiveToDo
from mastergoal.goals.models import PipelineToDo
from mastergoal.goals.models import NormalToDo
from mastergoal.goals.models import Strategy
from mastergoal.goals.models import ToDo
from mastergoal.goals.models import Link
from mastergoal.goals.models import Goal
from mastergoal.goals.utils import UserPassesProgressMonitorTestMixin
from mastergoal.goals.utils import UserPassesStrategyTestMixin
from mastergoal.goals.utils import UserPassesGoalTestMixin
from mastergoal.goals.utils import UserPassesLinkTestMixin
from mastergoal.goals.utils import UserPassesToDoTestMixin


# main views
class DashboardView(LoginRequiredMixin, ListView):
    template_name = "goals_goal_view.j2"
    model = Goal
    context_object_name = 'goals'

    def get_queryset(self):
        user = self.request.user
        goals = Goal.get_goals_user(user, user.goal_view_goal_choice)
        return goals


class SearchView(LoginRequiredMixin, TemplateView):
    template_name = 'goals_search_view.j2'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user = self.request.user
        all_goals = user.goals.all()
        all_strategies = Strategy.get_strategies_goals(all_goals, "ALL")
        query = self.request.GET['q']

        context['goals'] = all_goals.filter(name__icontains=query)
        context['strategies'] = all_strategies.filter(name__icontains=query)
        context['to_dos'] = ToDo \
            .get_to_dos_strategies(all_strategies, NormalToDo, 'ALL') \
            .filter(name__icontains=query)
        context['never_ending_to_dos'] = ToDo \
            .get_to_dos_strategies(all_strategies, NeverEndingToDo, 'ALL') \
            .filter(name__icontains=query)
        context['repetitive_to_dos'] = ToDo \
            .get_to_dos_strategies(all_strategies, RepetitiveToDo, 'ALL') \
            .filter(name__icontains=query)
        context['pipeline_to_dos'] = ToDo \
            .get_to_dos_strategies(all_strategies, PipelineToDo, 'ALL') \
            .filter(name__icontains=query)
        return context


class TestView(LoginRequiredMixin, TemplateView):
    template_name = "test.j2"


class ToDosView(LoginRequiredMixin, TemplateView):
    template_name = "goals_to_dos_view.j2"

    def get_context_data(self, **kwargs):
        context = super(ToDosView, self).get_context_data(**kwargs)
        user = self.request.user
        all_goals = user.goals.filter(is_archived=False)
        all_strategies = Strategy.get_strategies_goals(all_goals, "ALL")

        context['to_dos'] = ToDo \
            .get_to_dos_strategies(all_strategies,
                                   NormalToDo,
                                   user.normal_to_dos_choice,
                                   delta=user.to_dos_delta,
                                   include_archived_to_dos=self.request.user.show_archived_objects)
        context['repetitive_to_dos'] = ToDo \
            .get_to_dos_strategies(all_strategies,
                                   RepetitiveToDo,
                                   user.repetitive_to_dos_choice,
                                   delta=user.to_dos_delta,
                                   include_archived_to_dos=self.request.user.show_archived_objects)
        context['never_ending_to_dos'] = ToDo \
            .get_to_dos_strategies(all_strategies,
                                   NeverEndingToDo,
                                   user.never_ending_to_dos_choice,
                                   delta=user.to_dos_delta,
                                   include_archived_to_dos=self.request.user.show_archived_objects)
        context['pipeline_to_dos'] = ToDo \
            .get_to_dos_strategies(all_strategies,
                                   PipelineToDo,
                                   user.pipeline_to_dos_choice,
                                   delta=user.to_dos_delta,
                                   include_archived_to_dos=self.request.user.show_archived_objects)

        return context


class TreeView(LoginRequiredMixin, TemplateView):
    template_name = "goals_tree_view.j2"

    def get_context_data(self, **kwargs):
        context = super(TreeView, self).get_context_data(**kwargs)
        user = self.request.user
        all_goals = Goal.get_goals_user(user, user.treeview_goal_choice).prefetch_related('sub_goals')
        subgoal_pks = []
        for goal in list(all_goals):
            for master_goal in list(goal.master_goals.all()):
                if master_goal in all_goals:
                    subgoal_pks.append(goal.pk)
                    break
        tree = []
        master_goals = all_goals.exclude(pk__in=subgoal_pks)
        for goal in list(master_goals):
            goal_tree = goal.get_tree(
                normaltodo_choice=user.treeview_normaltodos_choice,
                repetitivetodo_choice=user.treeview_repetitivetodos_choice,
                neverendingtodo_choice=user.treeview_neverendingtodos_choice,
                pipelinetodo_choice=user.treeview_pipelinetodos_choice,
                goal_choice=user.treeview_goal_choice,
                strategy_choice=user.treeview_strategy_choice,
                monitor_choice=user.treeview_monitor_choice
            )
            tree.append(goal_tree)
        context['tree'] = tree
        return context


class StarView(LoginRequiredMixin, TemplateView):
    template_name = "goals_star_view.j2"

    def get_context_data(self, **kwargs):
        context = super(StarView, self).get_context_data(**kwargs)
        user = self.request.user

        sao = self.request.user.show_archived_objects

        context['goals'] = Goal.get_goals_user(user, user.goal_choice, sao)

        context['progress_monitors'] = ProgressMonitor.get_monitors_user(user, user.progress_monitor_choice, sao)

        context['links'] = Link.get_links_user(user, user.link_choice, sao)

        context['strategies'] = Strategy.get_strategies_user(user, user.strategy_choice, sao)

        context['to_dos'] = (
            ToDo
                .get_to_dos_user(user, NormalToDo, user.starview_normaltodos_choice, user.starview_todos_delta, sao)
                .order_by('is_done', 'has_failed', 'deadline', 'activate', 'name'))
        context['never_ending_to_dos'] = (
            ToDo
                .get_to_dos_user(user, NeverEndingToDo, user.starview_neverendingtodos_choice,
                                 user.starview_todos_delta,
                                 sao)
                .order_by('is_done', 'has_failed', 'deadline', 'activate', 'name')
        )
        context['repetitive_to_dos'] = (
            ToDo
                .get_to_dos_user(user, RepetitiveToDo, user.starview_repetitivetodos_choice, user.starview_todos_delta,
                                 sao)
                .order_by('is_done', 'has_failed', 'deadline', 'activate', 'name')
        )
        context['pipeline_to_dos'] = (
            ToDo
                .get_to_dos_user(user, PipelineToDo, user.starview_pipelinetodos_choice, user.starview_todos_delta, sao)
                .order_by('is_done', 'has_failed', 'deadline', 'activate', 'name')
        )

        return context


class AddView(LoginRequiredMixin, TemplateView):
    template_name = 'goals_add_view.j2'

    def get_context_data(self, **kwargs):
        context = super(AddView, self).get_context_data()
        return context


# detail views
class GoalView(LoginRequiredMixin, UserPassesGoalTestMixin, DetailView):
    template_name = "goals_goal.j2"
    model = Goal

    def get_context_data(self, **kwargs):
        context = super(GoalView, self).get_context_data(**kwargs)
        sao = self.request.user.show_archived_objects
        context['strategies'] = Strategy.get_strategies(self.object.strategies.all(), 'ALL', sao)
        context['master_goals'] = Goal.get_goals(self.object.master_goals.all(), 'ALL', sao)
        context['sub_goals'] = Goal.get_goals(self.object.sub_goals.all(), 'ALL', sao)
        context['progress_monitors'] = ProgressMonitor.get_monitors(self.object.progress_monitors.all(), 'ALL', sao)
        context['links'] = Link.get_links(self.object.sub_links.all(), 'ALL', sao)
        return context


class ProgressMonitorView(LoginRequiredMixin, UserPassesProgressMonitorTestMixin, DetailView):
    template_name = "goals_progress_monitor.j2"
    model = ProgressMonitor


class LinkView(LoginRequiredMixin, UserPassesLinkTestMixin, DetailView):
    template_name = "goals_link.j2"
    model = Link


class StrategyView(LoginRequiredMixin, UserPassesStrategyTestMixin, DetailView):
    template_name = "goals_strategy.j2"
    model = Strategy

    def get_context_data(self, **kwargs):
        context = super(StrategyView, self).get_context_data(**kwargs)
        context['goal'] = self.object.goal
        to_do_filter = Q(strategy=self.object)
        sao = self.request.user.show_archived_objects
        context["repetitive_to_dos"] = ToDo.get_to_dos(RepetitiveToDo.objects.filter(to_do_filter), 'ALL',
                                                       include_archived_to_dos=sao)
        context["never_ending_to_dos"] = ToDo.get_to_dos(NeverEndingToDo.objects.filter(to_do_filter), 'ALL',
                                                         include_archived_to_dos=sao)
        context["pipeline_to_dos"] = ToDo.get_to_dos(PipelineToDo.objects.filter(to_do_filter), 'ALL',
                                                     include_archived_to_dos=sao)
        context["to_dos"] = ToDo.get_to_dos(NormalToDo.objects.filter(to_do_filter), 'ALL', include_archived_to_dos=sao)
        return context


class ToDoView(LoginRequiredMixin, UserPassesToDoTestMixin, DetailView):
    template_name = "goals_to_do.j2"
    model = ToDo

    def get_context_data(self, **kwargs):
        context = super(ToDoView, self).get_context_data(**kwargs)
        context['strategy'] = self.object.strategy
        context['goal'] = context['strategy'].goal
        context['to_do'] = self.object
        context['to_do_prefix'] = ''
        return context


class RepetitiveToDoView(ToDoView):
    model = RepetitiveToDo

    def get_context_data(self, **kwargs):
        context = super(RepetitiveToDoView, self).get_context_data(**kwargs)
        context['to_do_prefix'] = 'repetitive_'
        return context


class NeverEndingToDoView(ToDoView):
    model = NeverEndingToDo

    def get_context_data(self, **kwargs):
        context = super(NeverEndingToDoView, self).get_context_data(**kwargs)
        context['to_do_prefix'] = 'never_ending_'
        return context


class PipelineToDoView(ToDoView):
    model = PipelineToDo

    def get_context_data(self, **kwargs):
        context = super(PipelineToDoView, self).get_context_data(**kwargs)
        context['to_do_prefix'] = 'pipeline_'
        return context


# all views
class AllGoalsView(LoginRequiredMixin, ListView):
    template_name = 'goals_all_goals_view.j2'
    context_object_name = 'goals'

    def get_queryset(self):
        return Goal.get_goals_user(self.request.user, "ALL", True).prefetch_related(
            'strategies', 'sub_links', 'master_links', 'master_goals', 'sub_goals')


class AllProgressMonitorsView(LoginRequiredMixin, ListView):
    template_name = 'goals_all_progress_monitors_view.j2'
    context_object_name = 'progress_monitors'

    def get_queryset(self):
        return ProgressMonitor.get_monitors_user(self.request.user, "ALL", True)


class AllLinksView(LoginRequiredMixin, ListView):
    template_name = 'goals_all_links_view.j2'
    context_object_name = 'links'

    def get_queryset(self):
        return Link.get_links_user(self.request.user, "ALL", True)


class AllStrategiesView(LoginRequiredMixin, ListView):
    template_name = 'goals_all_strategies_view.j2'
    context_object_name = 'strategies'

    def get_queryset(self):
        return Strategy.get_strategies_user(self.request.user, "ALL", True)


class AllToDosView(LoginRequiredMixin, TemplateView):
    template_name = "goals_all_to_dos_view.j2"

    def get_context_data(self, **kwargs):
        context = super(AllToDosView, self).get_context_data(**kwargs)
        all_strategies = Strategy.get_strategies_user(self.request.user, 'ALL', True)
        context['to_dos'] = ToDo.get_to_dos_strategies(all_strategies, NormalToDo, 'ALL',
                                                       include_archived_to_dos=True)
        context['repetitive_to_dos'] = ToDo.get_to_dos_strategies(all_strategies, RepetitiveToDo, 'ALL',
                                                                  include_archived_to_dos=True)
        context['never_ending_to_dos'] = ToDo.get_to_dos_strategies(all_strategies, NeverEndingToDo, 'ALL',
                                                                    include_archived_to_dos=True)
        context['pipeline_to_dos'] = ToDo.get_to_dos_strategies(all_strategies, PipelineToDo, 'ALL',
                                                                include_archived_to_dos=True)
        print(NeverEndingToDo.objects.all().first().strategy)
        print(NeverEndingToDo.objects.all().first().pk)
        print(context['never_ending_to_dos'])
        return context
