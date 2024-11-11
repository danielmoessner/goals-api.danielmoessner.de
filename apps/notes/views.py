from django.http import HttpRequest
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from apps.notes.models import Note


@login_required
def notes(request: HttpRequest):
    context = {
        "notes": Note.objects.filter(user=request.user)
    }
    return render(request, "notes/notes.html", context)
