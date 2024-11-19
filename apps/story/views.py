from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render

from apps.users.models import CustomUser


@login_required
def storyv(request: HttpRequest):
    assert isinstance(request.user, CustomUser)
    story = request.user.stories.first()
    return render(request, "story/story.html", {"story": story})
