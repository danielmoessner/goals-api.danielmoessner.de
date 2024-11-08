from typing import Any
from django import forms

from apps.todos.mixins import GetInstance
from apps.todos.models import NeverEndingTodo, NormalTodo, RepetitiveTodo, Todo
from django.utils import timezone

from apps.todos.utils import add_week, get_datetime_widget, get_end_of_week, get_specific_todo, get_start_of_week, setup_duration_field
from apps.users.models import CustomUser
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser

USER = AbstractBaseUser | AnonymousUser | CustomUser
OPTS = dict[str, Any]


class CreateTodo(GetInstance[NormalTodo], forms.ModelForm):
    nav = "create"

    class Meta:
        model = NormalTodo
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
            self.fields["deadline"].initial = get_end_of_week()
        elif variant == "next_week":
            self.fields["activate"].initial = add_week(get_start_of_week())
            self.fields["deadline"].initial = add_week(get_end_of_week())

    def ok(self):
        self.instance.user = self.user
        self.instance.save()
        return self.instance.pk


class CreateNeverEndingTodo(GetInstance[NeverEndingTodo], forms.ModelForm):
    nav = "create"
    text = "A never ending todo will reappear after the completion date + the duration time."
    submit = "Create"

    class Meta:
        model = NeverEndingTodo
        fields = ["name", "duration"]

    def __init__(self, user: USER, opts: OPTS, *args, **kwargs):
        assert isinstance(user, CustomUser)
        self.user = user
        super().__init__(*args, **kwargs)
        setup_duration_field(self.fields["duration"])

    def ok(self):
        self.instance.user = self.user
        self.instance.activate = timezone.now()
        self.instance.save()
        return self.instance.pk


class CreateRepetitiveTodo(GetInstance[RepetitiveTodo], forms.ModelForm):
    nav = "create"
    submit = "Create"

    class Meta:
        model = RepetitiveTodo
        fields = ["name", "duration", "repetitions"]
    
    def __init__(self, user: USER, opts: OPTS, *args, **kwargs):
        assert isinstance(user, CustomUser)
        self.user = user
        super().__init__(*args, **kwargs)
        setup_duration_field(self.fields["duration"])

    def ok(self):
        self.instance.user = self.user
        self.instance.activate = timezone.now()
        self.instance.deadline = timezone.now() + self.cleaned_data["duration"]
        self.instance.save()
        return self.instance.pk


class UpdateRepetitiveTodo(GetInstance[RepetitiveTodo], forms.ModelForm):
    class Meta:
        model = RepetitiveTodo
        fields = ["name", "status", "activate", "deadline", "repetitions"]

    def get_instance(self, pk: str, user: USER):
        return RepetitiveTodo.objects.get(pk=pk, user=user)

    def __init__(self, user: USER, opts: OPTS, *args, **kwargs):
        instance = self.get_instance(opts["pk"], user)
        super().__init__(*args, instance=instance, **kwargs)
        self.fields["activate"].widget = get_datetime_widget()
        self.fields["deadline"].widget = get_datetime_widget()

    def ok(self) -> int:
        self.instance.save()
        return self.instance.pk
    

class UpdateNormalTodo(GetInstance[NormalTodo], forms.ModelForm):
    class Meta:
        model = NormalTodo
        fields = ["name", "status", "activate", "deadline"]

    def get_instance(self, pk: str, user: USER):
        return NormalTodo.objects.get(pk=pk, user=user)

    def __init__(self, user: USER, opts: OPTS, *args, **kwargs):
        instance = self.get_instance(opts["pk"], user)
        super().__init__(*args, instance=instance, **kwargs)
        self.fields["activate"].widget = get_datetime_widget()
        self.fields["deadline"].widget = get_datetime_widget()

    def ok(self) -> int:
        self.instance.save()
        return self.instance.pk


class UpdateNeverEndingTodo(GetInstance[NeverEndingTodo], forms.ModelForm):
    class Meta:
        model = NeverEndingTodo
        fields = ["name", "status", "activate", "duration"]
    
    def get_instance(self, pk: str, user: USER):
        return NeverEndingTodo.objects.get(pk=pk, user=user)
    
    def __init__(self, user: USER, opts: OPTS, *args, **kwargs):
        instance = self.get_instance(opts["pk"], user)
        super().__init__(*args, instance=instance, **kwargs)
        self.fields["activate"].widget = get_datetime_widget()
    
    def ok(self) -> int:
        self.instance.save()
        return self.instance.pk


class DeleteTodo(GetInstance[NormalTodo], forms.ModelForm):
    text = "Are you sure you want to delete this todo?"
    submit = "Delete"

    class Meta:
        model = Todo
        fields = []
    
    def __init__(self, user: USER, opts: OPTS, *args, **kwargs):
        assert isinstance(user, CustomUser)
        instance = get_specific_todo(pk=opts["pk"], user=user)
        super().__init__(*args, instance=instance, **kwargs)

    def ok(self) -> int:
        self.instance.delete()
        return 0


class ToggleTodo(GetInstance[Todo], forms.ModelForm):
    class Meta:
        model = Todo
        fields = []

    def __init__(self, user: USER, opts: OPTS, *args, **kwargs):
        assert isinstance(user, CustomUser)
        instance = get_specific_todo(pk=opts["pk"], user=user)
        super().__init__(*args, instance=instance, **kwargs)
    
    def ok(self) -> int:
        self.instance.toggle()
        self.instance.save()
        return self.instance.pk
