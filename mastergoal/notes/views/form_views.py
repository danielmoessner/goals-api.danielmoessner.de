from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy

from mastergoal.notes.models import Note
from mastergoal.notes.utils import UserPassesNoteTestMixin
from mastergoal.notes.forms import NoteForm
from mastergoal.core.views import CustomAjaxFormMixin
from mastergoal.core.views import CustomGetFormMixin


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
