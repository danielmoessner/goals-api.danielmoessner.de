from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import ModelFormMixin
from django.core.exceptions import ImproperlyConfigured
from django.views.generic import View
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import redirect
from django.views import generic
from django.urls import reverse_lazy

from mastergoal.goals.models import ProgressMonitor
from mastergoal.goals.models import NeverEndingToDo
from mastergoal.goals.models import RepetitiveToDo
from mastergoal.goals.models import PipelineToDo
from mastergoal.goals.models import Strategy
from mastergoal.goals.models import ToDo
from mastergoal.goals.models import Goal
from mastergoal.goals.models import Link
from mastergoal.goals.utils import UserPassesProgressMonitorTestMixin
from mastergoal.goals.utils import UserPassesStrategyTestMixin
from mastergoal.goals.forms import NeverEndingToDoFailedForm
from mastergoal.goals.forms import RepetitiveToDoFailedForm
from mastergoal.goals.utils import UserPassesGoalTestMixin
from mastergoal.goals.utils import UserPassesToDoTestMixin
from mastergoal.goals.utils import UserPassesLinkTestMixin
from mastergoal.goals.forms import ProgressMonitorStepForm
from mastergoal.goals.forms import NeverEndingToDoDoneForm
from mastergoal.goals.forms import PipelineToDoFailedForm
from mastergoal.goals.forms import RepetitiveToDoDoneForm
from mastergoal.goals.forms import PipelineToDoDoneForm
from mastergoal.goals.forms import NeverEndingToDoForm
from mastergoal.goals.forms import ProgressMonitorForm
from mastergoal.goals.forms import RepetitiveToDoForm
from mastergoal.goals.forms import PipelineToDoForm
from mastergoal.goals.forms import ToDoFailedForm
from mastergoal.goals.forms import ToDoNotesForm
from mastergoal.goals.forms import ToDoDoneForm
from mastergoal.goals.forms import StrategyForm
from mastergoal.goals.forms import ToDoForm
from mastergoal.goals.forms import GoalForm
from mastergoal.goals.forms import LinkForm
from mastergoal.core.views import CustomSimpleAjaxFormMixin
from mastergoal.core.views import CustomAjaxFormMixin
from mastergoal.core.views import CustomGetFormMixin


class FieldsetFormContextMixin(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if 'form' not in context:
            raise ImproperlyConfigured(
                'There need to be a form in the context for the FieldsetFormContextMixin to work.')
        fieldsets = None
        form_class = self.get_form_class()
        if 'fieldsets' in form_class.Meta.__dict__:
            fieldsets = form_class.Meta.__dict__['fieldsets']
        context['form'].__dict__['fieldsets'] = fieldsets
        return context


# Goal
class GoalAdd(LoginRequiredMixin, FieldsetFormContextMixin, CustomAjaxFormMixin, CustomGetFormMixin,
              generic.CreateView):
    form_class = GoalForm
    model = Goal
    template_name = "snippets/fieldset_form.j2"


class GoalEdit(LoginRequiredMixin, FieldsetFormContextMixin, UserPassesGoalTestMixin, CustomAjaxFormMixin,
               CustomGetFormMixin, generic.UpdateView):
    form_class = GoalForm
    model = Goal
    template_name = "snippets/fieldset_form.j2"


class GoalDelete(LoginRequiredMixin, UserPassesGoalTestMixin, generic.DeleteView):
    model = Goal
    template_name = "snippets/delete.j2"
    success_url = reverse_lazy("goals:index")

    def get_context_data(self, **kwargs):
        context = super(GoalDelete, self).get_context_data(**kwargs)
        context['info'] = "All sub goals will be deleted. All strategies and sub strategies will be deleted. All sub " \
                          "to do's will be deleted"
        return context


class GoalStar(LoginRequiredMixin, UserPassesGoalTestMixin, generic.DetailView):
    model = Goal

    def get(self, request, *args, **kwargs):
        goal = self.get_object()
        goal.set_starred()
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


# Strategy
class StrategyAdd(LoginRequiredMixin, FieldsetFormContextMixin, CustomAjaxFormMixin, CustomGetFormMixin,
                  generic.CreateView):
    form_class = StrategyForm
    model = Strategy
    template_name = 'snippets/fieldset_form.j2'


class StrategyEdit(LoginRequiredMixin, UserPassesStrategyTestMixin, FieldsetFormContextMixin, CustomAjaxFormMixin,
                   CustomGetFormMixin, generic.UpdateView):
    form_class = StrategyForm
    model = Strategy
    template_name = 'snippets/fieldset_form.j2'


class StrategyDelete(LoginRequiredMixin, UserPassesStrategyTestMixin, generic.DeleteView):
    model = Strategy
    template_name = "snippets/delete.j2"
    success_url = reverse_lazy("goals:index")

    def get_context_data(self, **kwargs):
        context = super(StrategyDelete, self).get_context_data(**kwargs)
        context['info'] = "All to do's will be deleted."
        return context


class StrategyStar(LoginRequiredMixin, UserPassesStrategyTestMixin, ModelFormMixin, View):
    model = Strategy

    def get(self, request, *args, **kwargs):
        strategy = self.get_object()
        strategy.set_starred()
        return redirect('goals:strategy', pk=strategy.pk)


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
        self.objects = self.get_objects()
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
        self.object.get_all_before().update(end_day=self.object.activate)
        success_url = reverse_lazy("goals:strategy", args=[self.object.strategy.pk])
        self.objects.delete()
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


# NeverEndingToDo
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
