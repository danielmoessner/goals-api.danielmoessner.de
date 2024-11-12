from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render

from apps.achievements.models import Achievement


@login_required
def achievements(request: HttpRequest):
    context = {"achievements": Achievement.objects.filter(user=request.user)}
    return render(request, "achievements.html", context)
