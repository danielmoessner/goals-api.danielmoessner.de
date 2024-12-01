from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.goals.models import Goal


@login_required
def goals(request):
    all_goals = Goal.objects.filter(is_archived=False).prefetch_related("master_goals")
    goals: list[Goal] = []
    for g in all_goals:
        if len(g.master_goals.all()) == 0:
            goals.append(g)
    return render(request, "goals/goals.html", {"goals": goals})
