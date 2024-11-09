from django.http import HttpRequest
from django.shortcuts import  render
from apps.todos.models import NeverEndingTodo, NormalTodo, PipelineTodo, RepetitiveTodo, Todo
from django.contrib.auth.decorators import login_required

from apps.todos.utils import get_end_of_week, get_start_of_week
from django.db.models import Q
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
