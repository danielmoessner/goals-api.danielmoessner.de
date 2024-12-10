from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.goals.models import Goal
from apps.users.models import CustomUser
from apps.utils.functional import list_filter, list_map


class Leaf:
    def __init__(self, goal: Goal, children: list["Leaf"]):
        self.goal = goal
        self.children = children

    def __repr__(self) -> str:
        s = f"{self.goal.name}"
        for c in self.children:
            s += f"\n-{repr(c)}"
        return s

    @staticmethod
    def build(user: CustomUser) -> list["Leaf"]:
        goals_qs = Goal.objects.filter(user=user, is_archived=False).prefetch_related("master_goals", "sub_goals")
        goals_list = list(goals_qs)
        goals_dict = {g.pk: g for g in goals_list}
        root_goals = list_filter(goals_list, lambda g: len(g.master_goals.all()) == 0)
        root = list_map(root_goals, lambda g: Leaf.build_leaf(g, goals_dict))
        return root
    
    @staticmethod
    def build_leaf(goal: Goal, goals_dict: dict[int, Goal]):
        children = Leaf.build_children(goal, goals_dict)
        return Leaf(goal=goal, children=list(children))

    @staticmethod
    def build_children(goal: Goal, goals_dict: dict[int, Goal]):
        goals_qs = goal.sub_goals.all()
        goals_pks = list_map(goals_qs, lambda g: g.pk)
        for pk in goals_pks:
            if pk in goals_dict:
                goal = goals_dict[pk]
                yield Leaf.build_leaf(goal, goals_dict)
    

@login_required
def goals(request):
    assert isinstance(request.user, CustomUser)
    leafes = Leaf.build(request.user)
    print(leafes)
    return render(request, "goals/goals.html", {"leafes": leafes})
