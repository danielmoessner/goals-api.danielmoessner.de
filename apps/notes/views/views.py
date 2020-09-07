from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DetailView, ListView

from apps.notes.models import Note
from apps.notes.utils import UserPassesNoteTestMixin


# Create your views here.
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "notes_index.j2"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context["notes"] = self.request.user.notes.all()
        return context


class NoteView(LoginRequiredMixin, UserPassesNoteTestMixin, DetailView):
    template_name = "notes_note.j2"
    model = Note

    def get_context_data(self, **kwargs):
        context = super(NoteView, self).get_context_data(**kwargs)
        return context
