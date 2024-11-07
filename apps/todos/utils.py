from django import forms
from django.core.exceptions import ObjectDoesNotExist
from apps.todos.models import NeverEndingToDo, NormalToDo, RepetitiveToDo, PipelineToDo
from apps.users.models import CustomUser


def get_todo_in_its_proper_class(pk):
    if NormalToDo.objects.filter(pk=pk).exists():
        return NormalToDo.objects.get(pk=pk)
    elif NeverEndingToDo.objects.filter(pk=pk).exists():
        return NeverEndingToDo.objects.get(pk=pk)
    elif RepetitiveToDo.objects.filter(pk=pk).exists():
        return RepetitiveToDo.objects.get(pk=pk)
    elif PipelineToDo.objects.filter(pk=pk).exists():
        return PipelineToDo.objects.get(pk=pk)
    raise ObjectDoesNotExist()


from datetime import datetime, timedelta

def get_last_time_of_week():
    now = datetime.now()
    week_start = now - timedelta(days=now.weekday())
    end_of_week = (week_start + timedelta(days=6)).replace(hour=23, minute=59, second=59, microsecond=0)
    return end_of_week


def get_start_of_week():
    now = datetime.now()
    week_start = now - timedelta(days=now.weekday())
    week_start_with_time = (week_start).replace(hour=0, minute=0, second=0, microsecond=0)
    return week_start_with_time


def add_week(dt: datetime) -> datetime:
    return dt + timedelta(weeks=1)

def get_datetime_widget():
    return forms.DateTimeInput(
            attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
        )


def get_specific_todo(pk: int | str, user: CustomUser):
    try:
        return NormalToDo.objects.get(pk=pk, user=user)
    except ObjectDoesNotExist:
        pass
    try:
        return NeverEndingToDo.objects.get(pk=pk, user=user)
    except ObjectDoesNotExist:
        pass
    try:
        return RepetitiveToDo.objects.get(pk=pk, user=user)
    except ObjectDoesNotExist:
        pass
    try:
        return PipelineToDo.objects.get(pk=pk, user=user)
    except ObjectDoesNotExist:
        pass
    raise ObjectDoesNotExist()
