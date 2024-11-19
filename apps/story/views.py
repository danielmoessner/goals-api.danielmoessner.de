from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render

from apps.users.models import CustomUser


@login_required
def latest(request: HttpRequest):
    assert isinstance(request.user, CustomUser)
    story = request.user.stories.first()
    return render(request, "story/story.html", {"story": story})


@login_required
def older(request: HttpRequest):
    assert isinstance(request.user, CustomUser)
    show = request.GET.get("show", None)
    try:
        story = request.user.stories.get(pk=show)
    except Exception:
        story = None
    stories = request.user.stories.all()
    return render(request, "story/older.html", {"stories": stories, "story": story})
