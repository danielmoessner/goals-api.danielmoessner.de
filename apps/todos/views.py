from typing import Any, Protocol
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from apps.todos.forms import CreateNeverEndingTodo, CreateRepetitiveTodo, ToggleTodo, CreateNormalTodo, DeleteTodo, UpdateNeverEndingTodo, UpdateNormalTodo, UpdateRepetitiveTodo
from apps.todos.models import NeverEndingTodo, NormalTodo, PipelineTodo, RepetitiveTodo, Todo
from django.contrib.auth.decorators import login_required

from apps.todos.utils import get_end_of_week, get_start_of_week
from apps.users.models import CustomUser
from django.db.models import Q
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
from django.utils import timezone

class FormClass(Protocol):
    def __init__(self, user: CustomUser | AbstractBaseUser | AnonymousUser, opts: dict[str, Any], *args, **kwargs): ...

    def ok(self) -> int: ...

    def is_valid(self) -> bool: ...


def get_name(cls: type[object]):
    return cls.__name__


# improve to import automatically
FORMS: list[type[FormClass]] = [
    CreateNormalTodo,
    UpdateNormalTodo,
    UpdateNeverEndingTodo,
    DeleteTodo,
    ToggleTodo,
    CreateNeverEndingTodo,
    CreateRepetitiveTodo,
    UpdateRepetitiveTodo,
]

FORMS_DICT: dict[str, type[FormClass]] = {
    get_name(c): c for c in FORMS
}

NAVS = {
    "create": "create_nav.html"
}

class GetFormError(Exception):
    pass


def get_form_class(form_name: str | None) -> type[FormClass]:
    if form_name is None:
        raise GetFormError("form needs to be supplied")
    form_class = FORMS_DICT.get(form_name, None)
    if form_class is None:
        raise GetFormError(f"form with name '{form_name}' not found")
    return form_class


def form_view(request: HttpRequest, form_name: str) -> HttpResponse:
    if request.method not in ["GET", "POST"]:
        return HttpResponse("only get and post allowed", 400)
    
    success_url = request.GET.get("success", request.get_full_path())
    assert isinstance(success_url, str)
    cancel_url = request.GET.get("cancel_url")

    try:
        form_class = get_form_class(form_name)
    except GetFormError as e:
        return HttpResponse(str(e), 400)
    
    data = None
    if request.method == "POST":
        data = request.POST.dict()

    form = form_class(request.user, opts=request.GET.dict(), data=data)
    if request.method == "POST" and form.is_valid():
        ret = form.ok()
        success_url = success_url.replace("0", str(ret))
        return redirect(success_url)
    
    response = render(
        request, "form_view.html", {"form": form, 
                                    "cancel_url": cancel_url, 
                                    "nav": NAVS.get(getattr(form, "nav", ""), "")}
    )
    return response


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
