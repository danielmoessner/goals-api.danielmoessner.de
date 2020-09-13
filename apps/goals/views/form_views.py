from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import ModelFormMixin
from django.core.exceptions import ImproperlyConfigured
from django.views.generic import View
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import redirect
from django.views import generic
from django.urls import reverse_lazy

from apps.goals.models import ProgressMonitor
from apps.goals.models import NeverEndingToDo
from apps.goals.models import RepetitiveToDo
from apps.goals.models import PipelineToDo
from apps.goals.models import Strategy
from apps.goals.models import ToDo
from apps.goals.models import Goal
from apps.goals.models import Link
from apps.goals.utils import UserPassesProgressMonitorTestMixin
from apps.goals.utils import UserPassesStrategyTestMixin
from apps.goals.forms import NeverEndingToDoFailedForm
from apps.goals.forms import RepetitiveToDoFailedForm
from apps.goals.utils import UserPassesGoalTestMixin
from apps.goals.utils import UserPassesToDoTestMixin
from apps.goals.utils import UserPassesLinkTestMixin
from apps.goals.forms import ProgressMonitorStepForm
from apps.goals.forms import NeverEndingToDoDoneForm
from apps.goals.forms import PipelineToDoFailedForm
from apps.goals.forms import RepetitiveToDoDoneForm
from apps.goals.forms import PipelineToDoDoneForm
from apps.goals.forms import NeverEndingToDoForm
from apps.goals.forms import ProgressMonitorForm
from apps.goals.forms import RepetitiveToDoForm
from apps.goals.forms import PipelineToDoForm
from apps.goals.forms import ToDoFailedForm
from apps.goals.forms import ToDoNotesForm
from apps.goals.forms import ToDoDoneForm
from apps.goals.forms import StrategyForm
from apps.goals.forms import ToDoForm
from apps.goals.forms import GoalForm
from apps.goals.forms import LinkForm
from apps.core.views import CustomSimpleAjaxFormMixin
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


# NormalToDo
class ToDoAdd(LoginRequiredMixin, FieldsetFormContextMixin, CustomAjaxFormMixin, CustomGetFormMixin,
              generic.CreateView):
    form_class = ToDoForm
    model = ToDo
    template_name = 'snippets/fieldset_form.j2'


class ToDoEdit(LoginRequiredMixin, FieldsetFormContextMixin, UserPassesToDoTestMixin, CustomAjaxFormMixin,
               CustomGetFormMixin, generic.UpdateView):
    form_class = ToDoForm
    model = ToDo
    template_name = 'snippets/fieldset_form.j2'


class ToDoDelete(LoginRequiredMixin, UserPassesToDoTestMixin, generic.DeleteView):
    model = ToDo
    template_name = "snippets/delete.j2"
    success_url = reverse_lazy("goals:index")


class ToDoDone(LoginRequiredMixin, UserPassesToDoTestMixin, CustomSimpleAjaxFormMixin, CustomGetFormMixin,
               generic.UpdateView):
    model = ToDo
    form_class = ToDoDoneForm
    template_name = "snippets/form.j2"
    success_url = reverse_lazy("goals:index")


class ToDoFailed(LoginRequiredMixin, UserPassesToDoTestMixin, CustomSimpleAjaxFormMixin, CustomGetFormMixin,
                 generic.UpdateView):
    model = ToDo
    form_class = ToDoFailedForm
    template_name = "snippets/form.j2"
    success_url = reverse_lazy("goals:index")


class ToDoNotes(LoginRequiredMixin, UserPassesToDoTestMixin, CustomSimpleAjaxFormMixin, CustomGetFormMixin,
                generic.UpdateView):
    model = ToDo
    form_class = ToDoNotesForm
    template_name = "snippets/form.j2"
    success_url = reverse_lazy("goals:index")


# RepetitiveToDo
class RepetitiveToDoAdd(ToDoAdd):
    form_class = RepetitiveToDoForm
    model = RepetitiveToDo
    template_name = 'snippets/fieldset_form.j2'


class RepetitiveToDoEdit(ToDoEdit):
    form_class = RepetitiveToDoForm
    model = RepetitiveToDo
    template_name = 'snippets/fieldset_form.j2'


class RepetitiveToDoDelete(ToDoDelete):
    model = RepetitiveToDo
    template_name = "snippets/delete.j2"


class RepetitiveToDoListDelete(LoginRequiredMixin, UserPassesToDoTestMixin, generic.DeleteView):
    model = RepetitiveToDo
    template_name = 'snippets/delete_list.j2'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        print(self.object)
        self.objects = self.get_objects()
        print(self.objects)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['objects'] = self.objects
        return context

    def get_objects(self):
        return self.object.get_all_after()

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.objects = self.get_objects()
        success_url = reverse_lazy("goals:strategy", args=[self.object.strategy.pk])
        object_pks = [obj.pk for obj in self.objects]
        self.model.objects.filter(pk__in=object_pks).delete()
        return HttpResponseRedirect(success_url)


class RepetitiveToDoDone(ToDoDone):
    model = RepetitiveToDo
    form_class = RepetitiveToDoDoneForm


class RepetitiveToDoFailed(ToDoFailed):
    model = RepetitiveToDo
    form_class = RepetitiveToDoFailedForm


# NeverEndingToDo
class NeverEndingToDoAdd(ToDoAdd):
    form_class = NeverEndingToDoForm
    model = NeverEndingToDo
    template_name = 'snippets/fieldset_form.j2'


class NeverEndingToDoEdit(ToDoEdit):
    form_class = NeverEndingToDoForm
    model = NeverEndingToDo
    template_name = 'snippets/fieldset_form.j2'


class NeverEndingToDoDelete(ToDoDelete):
    model = NeverEndingToDo
    template_name = "snippets/delete.j2"


class NeverEndingToDoDone(ToDoDone):
    model = NeverEndingToDo
    form_class = NeverEndingToDoDoneForm


class NeverEndingToDoFailed(ToDoFailed):
    model = NeverEndingToDo
    form_class = NeverEndingToDoFailedForm


# PipelineToDo
class PipelineToDoAdd(ToDoAdd):
    form_class = PipelineToDoForm
    model = PipelineToDo
    template_name = 'snippets/fieldset_form.j2'


class PipelineToDoEdit(ToDoEdit):
    form_class = PipelineToDoForm
    model = PipelineToDo
    template_name = 'snippets/fieldset_form.j2'


class PipelineToDoDelete(ToDoDelete):
    model = PipelineToDo
    template_name = "snippets/delete.j2"


class PipelineToDoDone(ToDoDone):
    model = PipelineToDo
    form_class = PipelineToDoDoneForm


class PipelineToDoFailed(ToDoFailed):
    model = PipelineToDo
    form_class = PipelineToDoFailedForm
