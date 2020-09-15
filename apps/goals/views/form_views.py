from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import generic
from django.urls import reverse_lazy

from apps.goals.models import ProgressMonitor
from apps.goals.models import Goal
from apps.goals.models import Link
from apps.goals.utils import UserPassesProgressMonitorTestMixin
from apps.goals.utils import UserPassesGoalTestMixin
from apps.goals.utils import UserPassesLinkTestMixin
from apps.goals.forms import ProgressMonitorStepForm
from apps.goals.forms import ProgressMonitorForm
from apps.goals.forms import GoalForm
from apps.goals.forms import LinkForm
from apps.core.views import CustomAjaxFormMixin
from apps.core.views import CustomGetFormMixin
from apps.core.utils import FieldsetFormContextMixin


# Goal
class CreateGoal(LoginRequiredMixin, FieldsetFormContextMixin, CustomAjaxFormMixin, CustomGetFormMixin,
                 generic.CreateView):
    form_class = GoalForm
    model = Goal
    template_name = "snippets/fieldset_form.j2"


class UpdateGoal(LoginRequiredMixin, FieldsetFormContextMixin, UserPassesGoalTestMixin, CustomAjaxFormMixin,
                 CustomGetFormMixin, generic.UpdateView):
    form_class = GoalForm
    model = Goal
    template_name = "snippets/fieldset_form.j2"


class DeleteGoal(LoginRequiredMixin, UserPassesGoalTestMixin, generic.DeleteView):
    model = Goal
    template_name = "snippets/delete.j2"
    success_url = reverse_lazy("goals:index")

    def get_context_data(self, **kwargs):
        context = super(DeleteGoal, self).get_context_data(**kwargs)
        context['info'] = "All sub goals will be deleted. All strategies and sub strategies will be deleted. All sub " \
                          "to do's will be deleted"
        return context


class UpdateStarGoal(LoginRequiredMixin, UserPassesGoalTestMixin, generic.DetailView):
    model = Goal

    def get(self, request, *args, **kwargs):
        goal = self.get_object()
        goal.set_starred()
        return redirect('goals:goal', pk=goal.pk)


class UpdateArchiveGoal(LoginRequiredMixin, UserPassesGoalTestMixin, generic.DetailView):
    model = Goal

    def get(self, request, *args, **kwargs):
        goal = self.get_object()
        goal.set_archived()
        return redirect('goals:goal', pk=goal.pk)


# Milestone
class ProgressMonitorAdd(LoginRequiredMixin, FieldsetFormContextMixin, CustomAjaxFormMixin, CustomGetFormMixin,
                         generic.CreateView):
    form_class = ProgressMonitorForm
    model = ProgressMonitor
    template_name = 'snippets/fieldset_form.j2'


class ProgressMonitorEdit(LoginRequiredMixin, UserPassesProgressMonitorTestMixin, FieldsetFormContextMixin,
                          CustomAjaxFormMixin, CustomGetFormMixin, generic.UpdateView):
    form_class = ProgressMonitorForm
    model = ProgressMonitor
    template_name = 'snippets/fieldset_form.j2'


class ProgressMonitorDelete(LoginRequiredMixin, UserPassesProgressMonitorTestMixin, generic.DeleteView):
    model = ProgressMonitor
    template_name = "snippets/delete.j2"
    success_url = reverse_lazy("goals:index")


class ProgressMonitorStep(LoginRequiredMixin, UserPassesProgressMonitorTestMixin, CustomAjaxFormMixin,
                          CustomGetFormMixin, generic.UpdateView):
    form_class = ProgressMonitorStepForm
    model = ProgressMonitor
    template_name = "snippets/form.j2"


# Link
class LinkAdd(LoginRequiredMixin, FieldsetFormContextMixin, CustomAjaxFormMixin, CustomGetFormMixin,
              generic.CreateView):
    form_class = LinkForm
    model = Link
    template_name = 'snippets/fieldset_form.j2'


class LinkEdit(LoginRequiredMixin, UserPassesLinkTestMixin, FieldsetFormContextMixin, CustomAjaxFormMixin,
               CustomGetFormMixin, generic.UpdateView):
    form_class = LinkForm
    model = Link
    template_name = 'snippets/fieldset_form.j2'


class LinkDelete(LoginRequiredMixin, UserPassesLinkTestMixin, generic.DeleteView):
    model = Link
    template_name = "snippets/delete.j2"
    success_url = reverse_lazy("goals:index")
