from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, TemplateView
from apps.todos.models import ToDo


class ToDosView(LoginRequiredMixin, TemplateView):
    template_name = "todos/main.html"


class AllToDosView(LoginRequiredMixin, TemplateView):
    template_name = "todos/list.html"


class AddToDosView(LoginRequiredMixin, TemplateView):
    template_name = "todos/add.html"


class ToDoView(LoginRequiredMixin, DetailView):
    template_name = "todos/detail.html"
    model = ToDo
