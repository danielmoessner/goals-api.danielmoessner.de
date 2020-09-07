from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.db.models import Q
from django.views.generic.edit import ModelFormMixin

from apps.core.views import CustomAjaxFormMixin, CustomGetFormMixin
from apps.goals.forms import StrategyForm
from apps.goals.models import NeverEndingToDo
from apps.goals.models import ProgressMonitor
from apps.goals.models import RepetitiveToDo
from apps.goals.models import PipelineToDo
from apps.goals.models import NormalToDo
from apps.goals.models import Strategy
from apps.goals.models import ToDo
from apps.goals.models import Link
from apps.goals.models import Goal
from apps.goals.utils import UserPassesProgressMonitorTestMixin
from apps.goals.utils import UserPassesStrategyTestMixin
from apps.goals.utils import UserPassesGoalTestMixin
from apps.goals.utils import UserPassesLinkTestMixin
from apps.goals.utils import UserPassesToDoTestMixin
from apps.goals.views.form_views import FieldsetFormContextMixin


# main views
class SearchView(LoginRequiredMixin, TemplateView):
    template_name = 'goals/main/search.j2'

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
    template_name = "goals/main/to_dos.j2"

    def get_context_data(self, **kwargs):
        context = super(ToDosView, self).get_context_data(**kwargs)
        user = self.request.user
        all_goals = user.goals.all()
        if not self.request.user.show_archived_objects:
            all_goals = all_goals.filter(is_archived=False)
        all_strategies = Strategy.get_strategies_goals(all_goals, "ALL")

        context['to_dos'] = ToDo.get_to_dos_strategies(
            all_strategies,
            NormalToDo,
            user.normal_to_dos_choice,
            delta=user.to_dos_delta,
            include_archived_to_dos=self.request.user.show_archived_objects
        )
        context['repetitive_to_dos'] = ToDo.get_to_dos_strategies(
            all_strategies,
            RepetitiveToDo,
            user.repetitive_to_dos_choice,
            delta=user.to_dos_delta,
            include_archived_to_dos=self.request.user.show_archived_objects
        )
        context['never_ending_to_dos'] = ToDo.get_to_dos_strategies(
            all_strategies,
            NeverEndingToDo,
            user.never_ending_to_dos_choice,
            delta=user.to_dos_delta,
            include_archived_to_dos=self.request.user.show_archived_objects
        )
        context['pipeline_to_dos'] = ToDo.get_to_dos_strategies(
            all_strategies,
            PipelineToDo,
            user.pipeline_to_dos_choice,
            delta=user.to_dos_delta,
            include_archived_to_dos=self.request.user.show_archived_objects
        )

        return context


class TreeView(LoginRequiredMixin, TemplateView):
    template_name = "goals/main/tree.j2"

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
    template_name = "goals/main/star.j2"

    def get_context_data(self, **kwargs):
        context = super(StarView, self).get_context_data(**kwargs)
        user = self.request.user

        sao = self.request.user.show_archived_objects

        context['goals'] = Goal.get_goals_user(user, 'STAR', sao)

        context['progress_monitors'] = ProgressMonitor.get_monitors_user(user, 'STAR', sao)

        context['links'] = Link.get_links_user(user, 'STAR', sao)

        context['strategies'] = Strategy.get_strategies_user(user, 'STAR', sao)

        return context


class AddView(LoginRequiredMixin, TemplateView):
    template_name = 'goals/main/add.j2'

    def get_context_data(self, **kwargs):
        context = super(AddView, self).get_context_data()
        return context


# detail views
class ProgressMonitorView(LoginRequiredMixin, UserPassesProgressMonitorTestMixin, DetailView):
    template_name = "goals/detail/progress_monitor.j2"
    model = ProgressMonitor


class LinkView(LoginRequiredMixin, UserPassesLinkTestMixin, DetailView):
    template_name = "goals/detail/link.j2"
    model = Link


class ToDoView(LoginRequiredMixin, UserPassesToDoTestMixin, DetailView):
    template_name = "goals/detail/to_do.j2"
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


class AllProgressMonitorsView(LoginRequiredMixin, ListView):
    template_name = 'goals/list/progress_monitors.j2'
    context_object_name = 'progress_monitors'

    def get_queryset(self):
        return ProgressMonitor.get_monitors_user(self.request.user, "ALL", self.request.user.show_archived_objects)


class AllLinksView(LoginRequiredMixin, ListView):
    template_name = 'goals/list/links.j2'
    context_object_name = 'links'

    def get_queryset(self):
        return Link.get_links_user(self.request.user, "ALL", self.request.user.show_archived_objects)


class AllToDosView(LoginRequiredMixin, TemplateView):
    template_name = "goals/list/to_dos.j2"

    def get_context_data(self, **kwargs):
        context = super(AllToDosView, self).get_context_data(**kwargs)
        all_strategies = Strategy.get_strategies_user(
            self.request.user, 'ALL', self.request.user.show_archived_objects
        )
        context['to_dos'] = ToDo.get_to_dos_strategies(
            all_strategies, NormalToDo, 'ALL',
            include_archived_to_dos=self.request.user.show_archived_objects
        )
        context['repetitive_to_dos'] = ToDo.get_to_dos_strategies(
            all_strategies, RepetitiveToDo, 'ALL',
            include_archived_to_dos=self.request.user.show_archived_objects
        )
        context['never_ending_to_dos'] = ToDo.get_to_dos_strategies(
            all_strategies, NeverEndingToDo, 'ALL',
            include_archived_to_dos=self.request.user.show_archived_objects
        )
        context['pipeline_to_dos'] = ToDo.get_to_dos_strategies(
            all_strategies, PipelineToDo, 'ALL',
            include_archived_to_dos=self.request.user.show_archived_objects
        )
        return context


###
# Goal: Main, Detail, List
###
class MainGoal(LoginRequiredMixin, ListView):
    template_name = "goals/main/goal.j2"
    model = Goal
    context_object_name = 'goals'

    def get_queryset(self):
        user = self.request.user
        goals = Goal.get_goals_user(user, user.goal_view_goal_choice)
        return goals


class DetailGoal(LoginRequiredMixin, UserPassesGoalTestMixin, DetailView):
    template_name = "goals/detail/goal.j2"
    model = Goal

    def get_context_data(self, **kwargs):
        context = super(DetailGoal, self).get_context_data(**kwargs)
        sao = self.request.user.show_archived_objects
        context['strategies'] = Strategy.get_strategies(self.object.strategies.all(), 'ALL', sao)
        context['master_goals'] = Goal.get_goals(self.object.master_goals.all(), 'ALL', sao)
        context['sub_goals'] = Goal.get_goals(self.object.sub_goals.all(), 'ALL', sao)
        context['progress_monitors'] = ProgressMonitor.get_monitors(self.object.progress_monitors.all(), 'ALL', sao)
        context['links'] = Link.get_links(self.object.master_links.all(), 'ALL', sao)
        return context


class ListGoal(LoginRequiredMixin, ListView):
    template_name = 'goals/list/goals.j2'
    context_object_name = 'goals'

    def get_queryset(self):
        return Goal.get_goals_user(
            self.request.user, "ALL", self.request.user.show_archived_objects
        ).prefetch_related(
            'strategies', 'sub_links', 'master_links', 'master_goals', 'sub_goals'
        )


###
# Strategy: Detail, List, Create, Update, UpdateArchive, UpdateStar, Delete
###
class DetailStrategy(LoginRequiredMixin, UserPassesStrategyTestMixin, DetailView):
    template_name = "goals/detail/strategy.j2"
    model = Strategy

    def get_context_data(self, **kwargs):
        context = super(DetailStrategy, self).get_context_data(**kwargs)
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


class ListStrategy(LoginRequiredMixin, ListView):
    template_name = 'goals/list/strategies.j2'
    context_object_name = 'strategies'

    def get_queryset(self):
        return Strategy.get_strategies_user(
            self.request.user, "ALL", self.request.user.show_archived_objects
        )


class MainStrategy(LoginRequiredMixin, ListView):
    template_name = 'goals/main/strategy.j2'
    model = Strategy

    def get_queryset(self):
        return Strategy.get_strategies_user(
            self.request.user, self.request.user.strategy_main_choice, self.request.user.show_archived_objects
        )


class CreateStrategy(LoginRequiredMixin, FieldsetFormContextMixin, CustomAjaxFormMixin, CustomGetFormMixin,
                     generic.CreateView):
    form_class = StrategyForm
    model = Strategy
    template_name = 'snippets/fieldset_form.j2'


class UpdateStrategy(LoginRequiredMixin, UserPassesStrategyTestMixin, FieldsetFormContextMixin, CustomAjaxFormMixin,
                     CustomGetFormMixin, generic.UpdateView):
    form_class = StrategyForm
    model = Strategy
    template_name = 'snippets/fieldset_form.j2'


class DeleteStrategy(LoginRequiredMixin, UserPassesStrategyTestMixin, generic.DeleteView):
    model = Strategy
    template_name = "snippets/delete.j2"
    success_url = reverse_lazy("goals:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['info'] = "All to do's will be deleted."
        return context


class UpdateStarStrategy(LoginRequiredMixin, UserPassesStrategyTestMixin, ModelFormMixin, generic.View):
    model = Strategy

    def get(self, request, *args, **kwargs):
        strategy = self.get_object()
        strategy.set_starred()
        return redirect('goals:strategy', pk=strategy.pk)


class UpdateArchiveStrategy(LoginRequiredMixin, UserPassesStrategyTestMixin, ModelFormMixin, generic.View):
    model = Strategy

    def get(self, request, *args, **kwargs):
        strategy = self.get_object()
        strategy.set_archived()
        return redirect('goals:strategy', pk=strategy.pk)
