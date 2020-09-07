from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy

from apps.notes.models import Note
from apps.notes.utils import UserPassesNoteTestMixin
from apps.notes.forms import NoteForm
from apps.core.views import CustomAjaxFormMixin
from apps.core.views import CustomGetFormMixin


# Goal
class NoteAdd(LoginRequiredMixin, CustomAjaxFormMixin, CustomGetFormMixin, generic.CreateView):
    form_class = NoteForm
    model = Note
    template_name = "snippets/form.j2"


class NoteEdit(LoginRequiredMixin, UserPassesNoteTestMixin, CustomAjaxFormMixin, CustomGetFormMixin, generic.UpdateView):
    form_class = NoteForm
    model = Note
    template_name = "snippets/form.j2"


class NoteDelete(LoginRequiredMixin, UserPassesNoteTestMixin, generic.DeleteView):
    model = Note
    template_name = "snippets/delete.j2"
    success_url = reverse_lazy("notes:index")
