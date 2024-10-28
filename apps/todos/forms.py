from datetime import timedelta
from django import forms

from apps.todos.mixins import GetInstance
from apps.todos.models import NormalToDo, ToDo
from django.utils import timezone

class CreateTodo(GetInstance[NormalToDo], forms.ModelForm):
    class Meta:
        model = NormalToDo
        fields = ["name", "deadline"]

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields["deadline"].widget = forms.DateTimeInput(
            attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
        )
        self.fields["deadline"].initial = timezone.now() + timedelta(days=7)

    def ok(self):
        self.instance.activate = timezone.now()
        self.instance.user = self.user
        self.instance.save()
        return self.instance.pk


class UpdateTodo(GetInstance[NormalToDo], forms.ModelForm):
    class Meta:
        model = NormalToDo
        fields = ["name", "deadline", "notes"]

    @staticmethod
    def get_instance(pk: str, **kwargs):
        return NormalToDo.objects.get(pk=pk)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def ok(self) -> int:
        self.instance.save()
        return self.instance.pk


class DeleteTodo(GetInstance[NormalToDo], forms.ModelForm):
    class Meta:
        model = NormalToDo
        fields = []

    @staticmethod
    def get_instance(pk: str, **kwargs):
        return NormalToDo.objects.get(pk=pk)
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def ok(self) -> int:
        self.instance.delete()
        return 0


class ToggleTodo(GetInstance[ToDo], forms.ModelForm):
    class Meta:
        model = ToDo
        fields = []

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def get_instance(pk: str, **kwargs):
        return ToDo.objects.get(pk=pk)
    
    def ok(self) -> int:
        self.instance.toggle()
        self.instance.save()
        return self.instance.pk