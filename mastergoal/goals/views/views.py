from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.db.models import Q

from mastergoal.goals.models import NeverEndingToDo
from mastergoal.goals.models import ProgressMonitor
from mastergoal.goals.models import RepetitiveToDo
from mastergoal.goals.models import MultipleToDo
from mastergoal.goals.models import PipelineToDo
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
        return self.request.user.goals.exclude(progress=100)


class SearchView(LoginRequiredMixin, TemplateView):
    template_name = 'goals_search_view.j2'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user = self.request.user
        all_goals = user.goals.all()
        all_strategies = Strategy.objects.filter(goal__in=all_goals)
        query = self.request.GET['q']

        context['goals'] = all_goals.filter(name__icontains=query)
        context['strategies'] = all_strategies.filter(name__icontains=query)
        context['to_dos'] = ToDo\
            .get_to_dos(all_strategies, ToDo, 'ALL')\
            .filter(name__icontains=query)
        context['never_ending_to_dos'] = ToDo\
            .get_to_dos(all_strategies, NeverEndingToDo, 'ALL')\
            .filter(name__icontains=query)
        context['repetitive_to_dos'] = ToDo\
            .get_to_dos(all_strategies, RepetitiveToDo, 'ALL')\
            .filter(name__icontains=query)
        context['multiple_to_dos'] = ToDo\
            .get_to_dos(all_strategies, MultipleToDo, 'ALL')\
            .filter(name__icontains=query)
        context['pipeline_to_dos'] = ToDo\
            .get_to_dos(all_strategies, PipelineToDo, 'ALL')\
            .filter(name__icontains=query)
        return context


class TestView(LoginRequiredMixin, TemplateView):
    template_name = "test.j2"


class ToDosView(LoginRequiredMixin, TemplateView):
    template_name = "goals_to_dos_view.j2"

    def get_context_data(self, **kwargs):
        context = super(ToDosView, self).get_context_data(**kwargs)
        user = self.request.user
        all_goals = user.goals.all()
        all_strategies = Strategy.objects.filter(goal__in=all_goals)
        strategies = all_strategies.filter(is_starred=True)

        context['to_dos'] = ToDo.get_to_dos(all_strategies,
                                            ToDo,
                                            user.normal_to_dos_choice,
                                            delta=user.to_dos_delta,
                                            strategies=strategies)
        context['repetitive_to_dos'] = ToDo.get_to_dos(all_strategies,
                                                       RepetitiveToDo,
                                                       user.repetitive_to_dos_choice,
                                                       delta=user.to_dos_delta,
                                                       strategies=strategies)
        context['never_ending_to_dos'] = ToDo.get_to_dos(all_strategies,
                                                         NeverEndingToDo,
                                                         user.never_ending_to_dos_choice,
                                                         delta=user.to_dos_delta,
                                                         strategies=strategies)
        context['multiple_to_dos'] = ToDo.get_to_dos(all_strategies,
                                                     MultipleToDo,
                                                     user.multiple_to_dos_choice,
                                                     delta=user.to_dos_delta,
                                                     strategies=strategies)
        context['pipeline_to_dos'] = ToDo.get_to_dos(all_strategies,
                                                     PipelineToDo,
                                                     user.pipeline_to_dos_choice,
                                                     delta=user.to_dos_delta,
                                                     strategies=strategies)

        return context


class TreeView(LoginRequiredMixin, TemplateView):
    template_name = "goals_tree_view.j2"

    def get_context_data(self, **kwargs):
        context = super(TreeView, self).get_context_data(**kwargs)
        all_goals = self.request.user.goals.all()
        all_links = Link.objects.filter(sub_goal__in=all_goals, master_goal__in=all_goals)\
            .select_related('master_goal', 'sub_goal')
        no_master_goals = [link.sub_goal.pk for link in all_links]
        context["master_goals"] = all_goals.exclude(pk__in=no_master_goals).prefetch_related('sub_goals', 'strategies',
                                                                                             'sub_links')
        return context


class StarView(LoginRequiredMixin, TemplateView):
    template_name = "goals_star_view.j2"

    def get_context_data(self, **kwargs):
        context = super(StarView, self).get_context_data(**kwargs)
        user = self.request.user
        all_goals = user.goals.all()
        context['goals'] = Goal.get_goals(all_goals, user.goal_choice).prefetch_related('master_goals', 'sub_goals',
                                                                                        'strategies', 'master_links',
                                                                                        'sub_links')
        all_monitors = ProgressMonitor.objects.filter(goal__in=all_goals)
        context['progress_monitors'] = ProgressMonitor.get_monitors(all_monitors, user.progress_monitor_choice,
                                                                    context['goals']).select_related('goal')
        all_links = Link.objects.filter(master_goal__in=all_goals, sub_goal__in=all_goals)
        context['links'] = Link.get_links(all_links, user.link_choice, context['goals']).select_related('sub_goal',
                                                                                                        'master_goal')
        all_strategies = Strategy.objects.filter(goal__in=all_goals)
        context['strategies'] = Strategy.get_strategies(all_strategies, user.strategy_choice,
                                                        context['goals']).select_related('goal')
        all_goals = context['goals']
        for goal in context['goals']:
            all_goals = all_goals | goal.get_all_subgoals()
        all_strategies = Strategy.objects.filter(goal__in=all_goals) | context['strategies']
        context['to_dos'] = ToDo.get_to_dos(all_strategies,
                                            ToDo,
                                            user.starview_normaltodos_choice,
                                            user.starview_todos_delta)\
            .order_by('is_done', 'has_failed', 'deadline', 'activate', 'name')
        context['never_ending_to_dos'] = ToDo.get_to_dos(all_strategies,
                                                         NeverEndingToDo,
                                                         user.starview_neverendingtodos_choice,
                                                         user.starview_todos_delta)\
            .order_by('is_done', 'has_failed', 'deadline', 'activate', 'name')
        context['repetitive_to_dos'] = ToDo.get_to_dos(all_strategies,
                                                       RepetitiveToDo,
                                                       user.starview_repetitivetodos_choice,
                                                       user.starview_todos_delta)\
            .order_by('is_done', 'has_failed', 'deadline', 'activate', 'name')
        context['multiple_to_dos'] = ToDo.get_to_dos(all_strategies,
                                                     MultipleToDo,
                                                     user.starview_multipletodos_choice,
                                                     user.starview_todos_delta)\
            .order_by('is_done', 'has_failed', 'deadline', 'activate', 'name')
        context['pipeline_to_dos'] = ToDo.get_to_dos(all_strategies,
                                                     PipelineToDo,
                                                     user.starview_pipelinetodos_choice,
                                                     user.starview_todos_delta)\
            .order_by('is_done', 'has_failed', 'deadline', 'activate', 'name')

        return context


class AddView(LoginRequiredMixin, TemplateView):
    template_name = 'goals_add_view.j2'

    def get_context_data(self, **kwargs):
        context = super(AddView, self).get_context_data()
        return context


# specific views
class GoalView(LoginRequiredMixin, UserPassesGoalTestMixin, DetailView):
    template_name = "goals_goal.j2"
    model = Goal

    def get_context_data(self, **kwargs):
        context = super(GoalView, self).get_context_data(**kwargs)
        context['strategies'] = self.object.strategies.all().select_related('goal')
        context['master_goals'] = self.object.master_goals.all().prefetch_related('strategies', 'sub_goals',
                                                                                  'master_goals', 'master_links',
                                                                                  'sub_links')
        context['sub_goals'] = self.object.sub_goals.all().prefetch_related('strategies', 'sub_goals', 'master_goals',
                                                                            'master_links', 'sub_links')
        context['progress_monitors'] = self.object.progress_monitors.all()
        context['links'] = self.object.sub_links.select_related('master_goal', 'sub_goal')
        return context


class ProgressMonitorView(LoginRequiredMixin, UserPassesProgressMonitorTestMixin, DetailView):
    template_name = "goals_progress_monitor.j2"
    model = ProgressMonitor

    def get_context_data(self, **kwargs):
        context = super(ProgressMonitorView, self).get_context_data(**kwargs)
        context['progress_monitor'] = context['progressmonitor']
        return context


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
        context["repetitive_to_dos"] = RepetitiveToDo.objects.filter(to_do_filter)
        context["never_ending_to_dos"] = NeverEndingToDo.objects.filter(to_do_filter)
        context["multiple_to_dos"] = MultipleToDo.objects.filter(to_do_filter)
        context["pipeline_to_dos"] = PipelineToDo.objects.filter(to_do_filter)
        context["to_dos"] = ToDo.objects.filter(to_do_filter).exclude(Q(pk__in=context["repetitive_to_dos"]) | Q(
            pk__in=context["never_ending_to_dos"]) | Q(pk__in=context["multiple_to_dos"]) | Q(
            pk__in=context['pipeline_to_dos']))
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


class MultipleToDoView(ToDoView):
    model = MultipleToDo

    def get_context_data(self, **kwargs):
        context = super(MultipleToDoView, self).get_context_data(**kwargs)
        context['to_do_prefix'] = 'multiple_'
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
        return self.request.user.goals.all().prefetch_related('strategies', 'sub_links', 'master_links', 'master_goals',
                                                              'sub_goals')


class AllProgressMonitorsView(LoginRequiredMixin, ListView):
    template_name = 'goals_all_progress_monitors_view.j2'
    context_object_name = 'progress_monitors'

    def get_queryset(self):
        all_goals = self.request.user.goals.all()
        return ProgressMonitor.objects.filter(goal__in=all_goals).select_related('goal')


class AllLinksView(LoginRequiredMixin, ListView):
    template_name = 'goals_all_links_view.j2'
    context_object_name = 'links'

    def get_queryset(self):
        all_goals = self.request.user.goals.all()
        return Link.objects.filter(sub_goal__in=all_goals, master_goal__in=all_goals).select_related('master_goal',
                                                                                                     'sub_goal')


class AllStrategiesView(LoginRequiredMixin, ListView):
    template_name = 'goals_all_strategies_view.j2'
    context_object_name = 'strategies'

    def get_queryset(self):
        all_goals = self.request.user.goals.all()
        return Strategy.objects.filter(goal__in=all_goals).select_related('goal')


class AllToDosView(LoginRequiredMixin, TemplateView):
    template_name = "goals_all_to_dos_view.j2"

    def get_context_data(self, **kwargs):
        context = super(AllToDosView, self).get_context_data(**kwargs)
        user = self.request.user
        all_goals = user.goals.all()
        all_strategies = Strategy.objects.filter(goal__in=all_goals)
        context['to_dos'] = ToDo.get_to_dos(all_strategies, ToDo, 'ALL')\
            .order_by('is_done', 'has_failed', 'deadline', 'activate', 'name')
        context['repetitive_to_dos'] = ToDo.get_to_dos(all_strategies, RepetitiveToDo, 'ALL')\
            .order_by('is_done', 'has_failed', 'deadline', 'activate', 'name')
        context['never_ending_to_dos'] = ToDo.get_to_dos(all_strategies, NeverEndingToDo, 'ALL')\
            .order_by('is_done', 'has_failed', 'deadline', 'activate', 'name')
        context['multiple_to_dos'] = ToDo.get_to_dos(all_strategies, MultipleToDo, 'ALL')\
            .order_by('is_done', 'has_failed', 'deadline', 'activate', 'name')
        context['pipeline_to_dos'] = ToDo.get_to_dos(all_strategies, PipelineToDo, 'ALL')\
            .order_by('is_done', 'has_failed', 'deadline', 'activate', 'name')
        return context
