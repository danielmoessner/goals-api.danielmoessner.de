from typing import Any, Generic, TypeVar
from django import forms

from apps.todos.models import NeverEndingTodo, NormalTodo, PipelineTodo, RepetitiveTodo, Todo
from django.utils import timezone
from django.db import models
from apps.todos.utils import add_week, get_datetime_widget, get_end_of_week, get_specific_todo, get_start_of_week, setup_datetime_field, setup_duration_field
from apps.users.models import CustomUser
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser

USER = AbstractBaseUser | AnonymousUser | CustomUser
OPTS = dict[str, Any]
T = TypeVar("T", bound=models.Model)


class OptsUserInstance(Generic[T]):
    instance: T

    def init(self):
        pass
    
    def get_instance(self) -> models.Model | None:
        return None

    def __init__(self, user: USER, opts: OPTS, *args, **kwargs):
        assert isinstance(user, CustomUser)
        self.user = user
        self.opts = opts
        instance = self.get_instance()
        super().__init__(*args, instance=instance, **kwargs)  # type: ignore
        self.init()


class CreateNormalTodo(OptsUserInstance[NormalTodo], forms.ModelForm):
    nav = "create"

    class Meta:
        model = NormalTodo
        fields = ["name", "activate", "deadline"]

    def init(self):
        self.fields["activate"].widget = get_datetime_widget()
        self.fields["deadline"].widget = get_datetime_widget()
        variant = self.opts.get("variant", "this_week")
        if variant == "this_week":
            self.fields["activate"].initial = get_start_of_week()
            self.fields["deadline"].initial = get_end_of_week()
        elif variant == "next_week":
            self.fields["activate"].initial = add_week(get_start_of_week())
            self.fields["deadline"].initial = add_week(get_end_of_week())

    def ok(self):
        self.instance.user = self.user
        self.instance.save()
        return self.instance.pk


class CreateNeverEndingTodo(OptsUserInstance[NeverEndingTodo], forms.ModelForm):
    nav = "create"
    text = "A never ending todo will reappear after the completion date + the duration time."
    submit = "Create"

    class Meta:
        model = NeverEndingTodo
        fields = ["name", "duration"]

    def init(self):
        setup_duration_field(self.fields["duration"])

    def ok(self):
        self.instance.user = self.user
        self.instance.activate = timezone.now()
        self.instance.save()
        return self.instance.pk


class CreateRepetitiveTodo(OptsUserInstance[RepetitiveTodo], forms.ModelForm):
    nav = "create"
    submit = "Create"

    class Meta:
        model = RepetitiveTodo
        fields = ["name", "duration", "repetitions"]
    
    def init(self):
        setup_duration_field(self.fields["duration"])

    def ok(self):
        self.instance.user = self.user
        self.instance.activate = timezone.now()
        self.instance.deadline = timezone.now() + self.cleaned_data["duration"]
        self.instance.save()
        return self.instance.pk


class CreatePipelineTodo(OptsUserInstance[PipelineTodo], forms.ModelForm):
    nav = "create"
    submit = "Create"
    text = "A pipeline todo activates once its previous todo completes"

    class Meta:
        model = PipelineTodo
        fields = ["name", "previous"]

    def init(self):
        qs = Todo.objects.filter(status="ACTIVE", user=self.user).order_by("name")
        self.fields["previous"].queryset = qs # type: ignore


class UpdateRepetitiveTodo(OptsUserInstance[RepetitiveTodo], forms.ModelForm):
    class Meta:
        model = RepetitiveTodo
        fields = ["name", "status", "activate", "deadline", "repetitions"]

    def get_instance(self):
        return RepetitiveTodo.objects.get(pk=self.opts["pk"], user=self.user)
    
    def init(self):
        setup_datetime_field(self.fields["activate"])
        setup_datetime_field(self.fields["deadline"])

    def ok(self) -> int:
        self.instance.save()
        return self.instance.pk
    

class UpdateNormalTodo(OptsUserInstance[NormalTodo], forms.ModelForm):
    class Meta:
        model = NormalTodo
        fields = ["name", "status", "activate", "deadline"]

    def get_instance(self):
        return NormalTodo.objects.get(pk=self.opts["pk"], user=self.user)

    def init(self):
        setup_datetime_field(self.fields["activate"])
        setup_datetime_field(self.fields["deadline"])

    def ok(self) -> int:
        self.instance.save()
        return self.instance.pk


class UpdateNeverEndingTodo(OptsUserInstance[NeverEndingTodo], forms.ModelForm):
    class Meta:
        model = NeverEndingTodo
        fields = ["name", "status", "activate", "duration"]
    
    def get_instance(self):
        return NeverEndingTodo.objects.get(pk=self.opts["pk"], user=self.user)

    def init(self):
        setup_datetime_field(self.fields["activate"])
    
    def ok(self) -> int:
        self.instance.save()
        return self.instance.pk


class DeleteTodo(OptsUserInstance[NormalTodo], forms.ModelForm):
    text = "Are you sure you want to delete this todo?"
    submit = "Delete"

    class Meta:
        model = Todo
        fields = []
    
    def get_instance(self):
        return get_specific_todo(pk=self.opts["pk"], user=self.user)

    def ok(self) -> int:
        self.instance.delete()
        return 0


class ToggleTodo(OptsUserInstance[Todo], forms.ModelForm):
    class Meta:
        model = Todo
        fields = []
    
    def get_instance(self):
        return get_specific_todo(pk=self.opts["pk"], user=self.user)

    def ok(self) -> int:
        self.instance.toggle()
        self.instance.save()
        return self.instance.pk
