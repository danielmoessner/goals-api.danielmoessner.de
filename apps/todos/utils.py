from django.core.exceptions import ObjectDoesNotExist
from apps.todos.models import NeverEndingToDo, NormalToDo, RepetitiveToDo, PipelineToDo


def get_todo_in_its_proper_class(pk):
    if NormalToDo.objects.filter(pk=pk).exists():
        return NormalToDo.objects.get(pk=pk)
    elif NeverEndingToDo.objects.filter(pk=pk).exists():
        return NeverEndingToDo.objects.get(pk=pk)
    elif RepetitiveToDo.objects.filter(pk=pk).exists():
        return RepetitiveToDo.objects.get(pk=pk)
    elif PipelineToDo.objects.filter(pk=pk).exists():
        return PipelineToDo.objects.get(pk=pk)
    raise ObjectDoesNotExist


from django.utils import timezone
from datetime import datetime, timedelta

def get_last_time_of_week():
    """
    Returns the last moment (23:59:59) of the current week based on the current time.
    """
    now = datetime.now()
    week_start = now - timedelta(days=now.weekday())
    end_of_week = (week_start + timedelta(weeks=1)).replace(hour=23, minute=59, second=59, microsecond=0)
    return end_of_week
