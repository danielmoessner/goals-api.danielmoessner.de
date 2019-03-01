from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DetailView
from django.db.models import Q
from django.utils import timezone

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


def unfinished_filter():
    return Q(Q(activate__lte=timezone.now()) | Q(activate=None), is_done=False, has_failed=False)


def active_filter():
    return Q(activate__lte=timezone.now(), is_done=False, has_failed=False)


def overdue_filter():
    return Q(deadline__lte=timezone.now(), is_done=False, has_failed=False)


def related_filter(strategies):
    return Q(strategy__in=strategies, is_done=False, has_failed=False)


def delta_filter(delta):
    return Q(deadline__lte=timezone.now() + delta, activate__lte=timezone.now(), is_done=False, has_failed=False)


def orange_filter():
    return Q(activate__lte=timezone.now(), is_done=False, has_failed=False)


def add_to_dos_to_context(context, name, to_do_class, to_dos_filter, all_strategies, delta, strategies):
    all_to_dos = to_do_class.objects.filter(strategy__in=all_strategies)
    if to_do_class is ToDo:
        all_to_dos = to_do_class.objects.filter(strategy__in=all_strategies) \
            .exclude(pk__in=RepetitiveToDo.objects.filter(strategy__in=all_strategies)) \
            .exclude(pk__in=NeverEndingToDo.objects.filter(strategy__in=all_strategies)) \
            .exclude(pk__in=MultipleToDo.objects.filter(strategy__in=all_strategies)) \
            .exclude(pk__in=PipelineToDo.objects.filter(strategy__in=all_strategies))
    if to_dos_filter == "ALL":
        to_dos = all_to_dos
    elif to_dos_filter == "ACTIVE":
        to_dos = all_to_dos.filter(active_filter())
    elif to_dos_filter == "DELTA":
        to_dos = all_to_dos.filter(delta_filter(delta))
    elif to_dos_filter == "OVERDUE":
        to_dos = all_to_dos.filter(overdue_filter())
    elif to_dos_filter == "UNFINISHED":
        to_dos = all_to_dos.filter(unfinished_filter())
    elif to_dos_filter == "RELATED":
        to_dos = all_to_dos.filter(related_filter(strategies))
    elif to_dos_filter == "ORANGE":
        to_dos = all_to_dos.filter(orange_filter()).order_by('deadline')
        to_dos = [to_do for to_do in to_dos if to_do.get_color() in ['orange', 'red', 'blue']]
    else:  # None
        to_dos = to_do_class.objects.none()
    if to_dos_filter != "ORANGE":
        to_dos = to_dos.order_by('deadline')
    context[name + "to_dos"] = to_dos


# views
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "goals_index.j2"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context["goals"] = self.request.user.goals.exclude(progress=100)\
            .prefetch_related('master_goals', 'sub_goals', 'strategies')
        context['links'] = Link.objects.filter(Q(sub_goal__in=context['goals']) & Q(master_goal__in=context['goals']))\
            .select_related('master_goal', 'sub_goal')
        context["strategies"] = Strategy.objects.filter(goal__in=context['goals']).exclude(progress=100)\
            .select_related('goal')
        to_do_filter = Q(is_done=False, has_failed=False, strategy__in=context['strategies'])
        context["repetitive_to_dos"] = RepetitiveToDo.objects.filter(to_do_filter)
        context["never_ending_to_dos"] = NeverEndingToDo.objects.filter(to_do_filter)
        context["multiple_to_dos"] = MultipleToDo.objects.filter(to_do_filter)
        context["pipeline_to_dos"] = PipelineToDo.objects.filter(to_do_filter).order_by('deadline')
        context["to_dos"] = ToDo.objects.filter(to_do_filter).exclude(Q(pk__in=context["repetitive_to_dos"]) | Q(
            pk__in=context["never_ending_to_dos"]) | Q(pk__in=context["multiple_to_dos"]) | Q(
            pk__in=context['pipeline_to_dos'])).order_by('deadline')
        no_master_goals = [link.sub_goal.pk for link in Link.objects.select_related('sub_goal')]
        context["master_goals"] = context['goals'].exclude(pk__in=no_master_goals)
        context['progress_monitors'] = ProgressMonitor.objects.filter(goal__in=context['goals']).exclude(progress=100)\
            .select_related('goal')
        return context


class ToDosView(LoginRequiredMixin, TemplateView):
    template_name = "goals_to_dos_view.j2"

    def get_context_data(self, **kwargs):
        context = super(ToDosView, self).get_context_data(**kwargs)
        user = self.request.user
        all_goals = user.goals.all()
        all_strategies = Strategy.objects.filter(goal__in=all_goals)
        strategies = all_strategies.filter(is_starred=True)
        add_to_dos_to_context(context, "", ToDo, user.normal_to_dos_choice,
                              all_strategies, user.to_dos_delta, strategies)
        add_to_dos_to_context(context, "repetitive_", RepetitiveToDo, user.repetitive_to_dos_choice,
                              all_strategies, user.to_dos_delta, strategies)
        add_to_dos_to_context(context, "never_ending_", NeverEndingToDo, user.never_ending_to_dos_choice,
                              all_strategies, user.to_dos_delta, strategies)
        add_to_dos_to_context(context, "multiple_", MultipleToDo, user.multiple_to_dos_choice,
                              all_strategies, user.to_dos_delta, strategies)
        add_to_dos_to_context(context, "pipeline_", PipelineToDo, user.pipeline_to_dos_choice,
                              all_strategies, user.to_dos_delta, strategies)
        return context


class AllToDosView(LoginRequiredMixin, TemplateView):
    template_name = "goals_to_dos_view.j2"

    def get_context_data(self, **kwargs):
        context = super(AllToDosView, self).get_context_data(**kwargs)
        user = self.request.user
        all_goals = user.goals.all()
        all_strategies = Strategy.objects.filter(goal__in=all_goals)
        add_to_dos_to_context(context, "", ToDo, "UNFINISHED", all_strategies, None, None)
        add_to_dos_to_context(context, "repetitive_", RepetitiveToDo, "UNFINISHED", all_strategies, None, None)
        add_to_dos_to_context(context, "never_ending_", NeverEndingToDo, "UNFINISHED", all_strategies, None, None)
        add_to_dos_to_context(context, "multiple_", MultipleToDo, "UNFINISHED", all_strategies, None, None)
        add_to_dos_to_context(context, "pipeline_", PipelineToDo, "UNFINISHED", all_strategies, None, None)
        return context


class TreeView(LoginRequiredMixin, TemplateView):
    template_name = "goals_tree_view.j2"

    def get_context_data(self, **kwargs):
        context = super(TreeView, self).get_context_data(**kwargs)
        no_master_goals = [link.sub_goal.pk for link in Link.objects.select_related('sub_goal')]
        context["master_goals"] = self.request.user.goals.all().exclude(pk__in=no_master_goals).prefetch_related(
            'sub_goals', 'strategies')
        return context


class StarView(LoginRequiredMixin, TemplateView):
    template_name = "goals_star_view.j2"

    def get_context_data(self, **kwargs):
        context = super(StarView, self).get_context_data(**kwargs)
        user = self.request.user

        all_goals = user.goals.all()
        if user.goal_choice == "ALL":
            goals = all_goals
        elif user.goal_choice == "STAR":
            goals = all_goals.filter(is_starred=True)
        elif user.goal_choice == "UNREACHED":
            goals = all_goals.exclude(progress=100)
        elif user.goal_choice == "ACHIEVED":
            goals = all_goals.filter(progress=100)
        elif user.goal_choice == "DEPTH" and False:
            goals = None
        else:  # None
            goals = Goal.objects.none()
        context['goals'] = goals.prefetch_related('master_goals', 'sub_goals', 'strategies')

        all_progress_monitors = ProgressMonitor.objects.filter(goal__in=all_goals)
        if user.progress_monitor_choice == "ALL":
            progress_monitors = all_progress_monitors
        elif user.progress_monitor_choice == "UNREACHED":
            progress_monitors = all_progress_monitors.exclude(progress=100)
        elif user.progress_monitor_choice == "LOADED":
            progress_monitors = all_progress_monitors.filter(progress=100)
        elif user.progress_monitor_choice == "RELATED":
            progress_monitors = all_progress_monitors.filter(goal__in=goals)
        else:  # None
            progress_monitors = ProgressMonitor.objects.none()
        context['progress_monitors'] = progress_monitors.select_related('goal')

        all_links = Link.objects.filter(master_goal__in=all_goals, sub_goal__in=all_goals)
        if user.link_choice == "ALL":
            links = all_links
        elif user.link_choice == "RELATED":
            links = all_links.filter(Q(master_goal__in=goals) | Q(sub_goal__in=goals))
        elif user.link_choice == "XRELATED":
            links = all_links.filter(master_goal__in=goals, sub_goal__in=goals)
        else:  # None
            links = Link.objects.none()
        context['links'] = links.select_related('sub_goal', 'master_goal')

        all_strategies = Strategy.objects.filter(goal__in=all_goals)
        if user.strategy_choice == "ALL":
            strategies = all_strategies
        elif user.strategy_choice == "STAR":
            strategies = all_strategies.filter(is_starred=True)
        elif user.strategy_choice == "RELATED":
            strategies = all_strategies.filter(goal__in=goals)
        else:  # None
            strategies = Strategy.objects.none()
        context['strategies'] = strategies.select_related('goal')

        return context


class GoalView(LoginRequiredMixin, UserPassesGoalTestMixin, DetailView):
    template_name = "goals_goal.j2"
    model = Goal

    def get_context_data(self, **kwargs):
        context = super(GoalView, self).get_context_data(**kwargs)
        context['strategies'] = self.object.strategies.all().select_related('goal')
        context['master_goals'] = self.object.master_goals.all().prefetch_related('strategies', 'sub_goals',
                                                                                  'master_goals')
        context['sub_goals'] = self.object.sub_goals.all().prefetch_related('strategies', 'sub_goals', 'master_goals')
        context['progress_monitors'] = self.object.progress_monitors.all()
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
        context["repetitive_to_dos"] = RepetitiveToDo.objects.filter(to_do_filter).order_by('deadline')
        context["never_ending_to_dos"] = NeverEndingToDo.objects.filter(to_do_filter).order_by('deadline')
        context["multiple_to_dos"] = MultipleToDo.objects.filter(to_do_filter).order_by('deadline')
        context["pipeline_to_dos"] = PipelineToDo.objects.filter(to_do_filter).order_by('deadline')
        context["to_dos"] = ToDo.objects.filter(to_do_filter).exclude(Q(pk__in=context["repetitive_to_dos"]) | Q(
            pk__in=context["never_ending_to_dos"]) | Q(pk__in=context["multiple_to_dos"]) | Q(
            pk__in=context['pipeline_to_dos'])).order_by('deadline')
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
