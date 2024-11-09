from typing import Any, Protocol
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from apps.todos.forms import CreateNeverEndingTodo, CreatePipelineTodo, CreateRepetitiveTodo, ToggleTodo, CreateNormalTodo, DeleteTodo, UpdateNeverEndingTodo, UpdateNormalTodo, UpdateRepetitiveTodo
from apps.todos.models import NeverEndingTodo, NormalTodo, PipelineTodo, RepetitiveTodo, Todo
from django.contrib.auth.decorators import login_required

from apps.todos.utils import get_end_of_week, get_start_of_week
from apps.users.models import CustomUser
from django.db.models import Q
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
from django.utils import timezone




@login_required
def todos(request: HttpRequest):
    todos = []
    kind = request.GET.get("kind", "week")
    for cls in [NormalTodo, PipelineTodo, NeverEndingTodo, RepetitiveTodo]:
        f = Q()
        if kind == "week":
            start_of_week = get_start_of_week()
            end_of_week = get_end_of_week()
            now = timezone.now()
            f = Q(activate__lte=now, status="ACTIVE") | Q(completed__gte=start_of_week, completed__lte=end_of_week)
        elif kind == "activated":
            f = Q(activate__lte=timezone.now())
        elif kind == "open":
            f = Q(status="ACTIVE") 
        
        todos += Todo.get_to_dos_user(request.user, cls).filter(f)
    return render(
        request, "todos.html", {"todos": todos}
    )
