from typing import Any
from django import forms

from apps.todos.mixins import GetInstance
from apps.todos.models import NeverEndingToDo, NormalToDo, ToDo
from django.utils import timezone

from apps.todos.utils import add_week, get_datetime_widget, get_last_time_of_week, get_start_of_week
from apps.users.models import CustomUser
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser

USER = AbstractBaseUser | AnonymousUser | CustomUser
OPTS = dict[str, Any]


class CreateTodo(GetInstance[NormalToDo], forms.ModelForm):
    nav = "create"

    class Meta:
        model = NormalToDo
        fields = ["name", "activate", "deadline"]

    def __init__(self, user: USER, opts: OPTS, *args, **kwargs):
        assert isinstance(user, CustomUser)
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields["activate"].widget = get_datetime_widget()
        self.fields["deadline"].widget = get_datetime_widget()
        variant = opts.get("variant", "this_week")
        if variant == "this_week":
            self.fields["activate"].initial = get_start_of_week()
            self.fields["deadline"].initial = get_last_time_of_week()
        elif variant == "next_week":
            self.fields["activate"].initial = add_week(get_start_of_week())
            self.fields["deadline"].initial = add_week(get_last_time_of_week())

    def ok(self):
        self.instance.activate = timezone.now()
        self.instance.user = self.user
        self.instance.save()
        return self.instance.pk


class CreateNeverEndingTodo(GetInstance[NeverEndingToDo], forms.ModelForm):
    nav = "create"
    text = "A never ending todo will reappear after the completion date + the duration time."
    submit = "Create"

    class Meta:
        model = NeverEndingToDo
        fields = ["name", "duration"]

    def __init__(self, user: USER, opts: OPTS, *args, **kwargs):
        assert isinstance(user, CustomUser)
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields["duration"].help_text = "Use 7d for 7 days"

    def ok(self):
        return 0


class UpdateTodo(GetInstance[NormalToDo], forms.ModelForm):
    class Meta:
        model = NormalToDo
        fields = ["name", "status", "notes", "activate", "deadline"]

    @staticmethod
    def get_instance(pk: str, user: USER):
        return NormalToDo.objects.get(pk=pk, user=user)

    def __init__(self, user: USER, opts: OPTS, *args, **kwargs):
        instance = UpdateTodo.get_instance(opts["pk"], user)
        super().__init__(*args, instance=instance, **kwargs)
        self.fields["activate"].widget = get_datetime_widget()
        self.fields["deadline"].widget = get_datetime_widget()

    def ok(self) -> int:
        self.instance.save()
        return self.instance.pk


class DeleteTodo(GetInstance[NormalToDo], forms.ModelForm):
    text = "Are you sure you want to delete this todo?"
    submit = "Delete"

    class Meta:
        model = NormalToDo
        fields = []
    
    def __init__(self, user: USER, opts: OPTS, *args, **kwargs):
        instance = UpdateTodo.get_instance(opts["pk"], user)
        super().__init__(*args, instance=instance, **kwargs)

    def ok(self) -> int:
        self.instance.delete()
        return 0


class ToggleTodo(GetInstance[ToDo], forms.ModelForm):
    class Meta:
        model = ToDo
        fields = []

    def __init__(self, user: USER, opts: OPTS, *args, **kwargs):
        instance = UpdateTodo.get_instance(opts["pk"], user)
        super().__init__(*args, instance=instance, **kwargs)
    
    def ok(self) -> int:
        self.instance.toggle()
        self.instance.save()
        return self.instance.pk
