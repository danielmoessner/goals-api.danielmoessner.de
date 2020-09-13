from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize
from django.db.models import Q
from django.utils import timezone
from django.views.generic import DetailView, TemplateView
from apps.todos.models import NeverEndingToDo, RepetitiveToDo, PipelineToDo, ToDo, NormalToDo
from apps.todos.forms import NeverEndingToDoFailedForm, RepetitiveToDoFailedForm, NeverEndingToDoDoneForm, \
    PipelineToDoFailedForm, PipelineToDoDoneForm, RepetitiveToDoDoneForm, NeverEndingToDoForm, RepetitiveToDoForm, \
    PipelineToDoForm, NormalToDoFailedForm, ToDoNotesForm, NormalToDoDoneForm, NormalToDoForm, ToDoDoneForm, \
    ToDoStatusForm, ToDoIsArchivedForm
from apps.todos.utils import UserPassesToDoTestMixin, get_todo_in_its_proper_class
from django.shortcuts import HttpResponseRedirect
from apps.core.views import CustomSimpleAjaxFormMixin, CustomAjaxFormMixin, CustomGetFormMixin
from apps.core.utils import FieldsetFormContextMixin
from django.views import generic
from django.urls import reverse_lazy


# main
class ToDosView(LoginRequiredMixin, TemplateView):
    template_name = "todos/main.html"

    def get_context_data(self, **kwargs):
        context = super(ToDosView, self).get_context_data(**kwargs)
        user = self.request.user
        normal_to_dos = ToDo.get_to_dos_user(
            user,
            NormalToDo,
            user.normal_to_dos_choice,
            delta=user.to_dos_delta,
            include_archived_to_dos=self.request.user.show_archived_objects
        )
        repetitive_to_dos = ToDo.get_to_dos_user(
            user,
            RepetitiveToDo,
            user.repetitive_to_dos_choice,
            delta=user.to_dos_delta,
            include_archived_to_dos=self.request.user.show_archived_objects
        )
        never_ending_to_dos = ToDo.get_to_dos_user(
            user,
            NeverEndingToDo,
            user.never_ending_to_dos_choice,
            delta=user.to_dos_delta,
            include_archived_to_dos=self.request.user.show_archived_objects
        )
        pipeline_to_dos = ToDo.get_to_dos_user(
            user,
            PipelineToDo,
            user.pipeline_to_dos_choice,
            delta=user.to_dos_delta,
            include_archived_to_dos=self.request.user.show_archived_objects
        )
        to_dos = ToDo.objects.filter(
            Q(pk__in=normal_to_dos.values('pk')) |
            Q(pk__in=repetitive_to_dos) |
            Q(pk__in=never_ending_to_dos.values('pk')) |
            Q(pk__in=pipeline_to_dos.values('pk'))
        )
        context['to_dos'] = serialize('json', to_dos)
        done_to_dos = ToDo.get_to_dos_user(
            user,
            ToDo,
            'ALL',
            include_archived_to_dos=True
        ).filter(
            completed__contains=timezone.now().date()
        )
        context['done_to_dos'] = serialize('json', done_to_dos)
        return context


# list
class AllToDosView(LoginRequiredMixin, TemplateView):
    template_name = "todos/list.html"


# detail
class ToDoView(LoginRequiredMixin, UserPassesToDoTestMixin, DetailView):
    template_name = "todos/detail.html"
    model = ToDo

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj = get_todo_in_its_proper_class(pk=obj.pk)
        return obj

    def get_context_data(self, **kwargs):
        context = super(ToDoView, self).get_context_data(**kwargs)
        context['todo'] = self.object.get_json()
        return context


class NormalToDoView(ToDoView):
    model = NormalToDo

    def get_context_data(self, **kwargs):
        context = super(NormalToDoView, self).get_context_data(**kwargs)
        context['to_do_prefix'] = 'normal_'
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


# ToDoForms
class ToDoAdd(LoginRequiredMixin, FieldsetFormContextMixin, CustomAjaxFormMixin, CustomGetFormMixin,
              generic.CreateView):
    model = ToDo
    template_name = 'snippets/fieldset_form.j2'


class ToDoEdit(LoginRequiredMixin, FieldsetFormContextMixin, UserPassesToDoTestMixin, CustomAjaxFormMixin,
               CustomGetFormMixin, generic.UpdateView):
    model = ToDo
    template_name = 'snippets/fieldset_form.j2'


class ToDoDelete(LoginRequiredMixin, UserPassesToDoTestMixin, generic.DeleteView):
    model = ToDo
    template_name = "snippets/delete.j2"
    success_url = reverse_lazy("todos:all_to_dos_view")


class ToDoDone(LoginRequiredMixin, UserPassesToDoTestMixin, CustomSimpleAjaxFormMixin, generic.UpdateView):
    model = ToDo
    form_class = ToDoDoneForm
    template_name = "snippets/form.j2"


class ToDoFailed(LoginRequiredMixin, UserPassesToDoTestMixin, CustomSimpleAjaxFormMixin, CustomGetFormMixin,
                 generic.UpdateView):
    model = ToDo
    template_name = "snippets/form.j2"
    success_url = reverse_lazy("todos:all_to_dos_view")


class ToDoNotes(LoginRequiredMixin, UserPassesToDoTestMixin, CustomSimpleAjaxFormMixin, CustomGetFormMixin,
                generic.UpdateView):
    model = ToDo
    form_class = ToDoNotesForm
    template_name = "snippets/form.j2"
    success_url = reverse_lazy("todos:all_to_dos_view")


class ToDoStatus(LoginRequiredMixin, UserPassesToDoTestMixin, CustomSimpleAjaxFormMixin, generic.UpdateView):
    model = ToDo
    form_class = ToDoStatusForm
    template_name = "snippets/form.j2"


class ToDoIsArchived(LoginRequiredMixin, UserPassesToDoTestMixin, CustomSimpleAjaxFormMixin, generic.UpdateView):
    model = ToDo
    form_class = ToDoIsArchivedForm
    template_name = "snippets/form.j2"


class ToDoUpdate(LoginRequiredMixin, generic.DetailView):
    model = ToDo

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return HttpResponseRedirect(self.object.get_update_url())

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj = get_todo_in_its_proper_class(pk=obj.pk)
        return obj


# NormalToDo
class NormalToDoAdd(ToDoAdd):
    form_class = NormalToDoForm
    model = NormalToDo


class NormalToDoEdit(ToDoEdit):
    form_class = NormalToDoForm
    model = NormalToDo


class NormalToDoDelete(ToDoDelete):
    model = NormalToDo


class NormalToDoDone(ToDoDone):
    model = NormalToDo
    form_class = NormalToDoDoneForm


class NormalToDoFailed(ToDoFailed):
    model = NormalToDo
    form_class = NormalToDoFailedForm


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
        success_url = reverse_lazy("todos:all_to_dos_view")
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
