from django import forms
from django.db import transaction
from django.db.models.base import Model as Model

from apps.goals.models import Goal
from apps.todos.utils import setup_datetime_field
from config.mixins import OptsUserInstance


class CreateGoal(OptsUserInstance[Goal], forms.ModelForm):
    navs = ["goals"]
    parent = forms.ModelChoiceField(queryset=Goal.objects.none())
    field_order = ["parent", "name"]

    class Meta:
        fields = ["name", "why", "impact", "deadline"]
        model = Goal

    def init(self):
        setup_datetime_field(self.fields["deadline"])
        self.fields["parent"].queryset = Goal.objects.filter(user=self.user)  # type: ignore

    def ok(self):
        self.instance.user = self.user
        parent: Goal | None = self.cleaned_data["parent"]
        with transaction.atomic():
            self.instance.save()
            if parent:
                parent.sub_goals.add(self.instance)
        return self.instance.pk


class UpdateGoal(OptsUserInstance[Goal], forms.ModelForm):
    navs = ["goals"]
    parent = forms.ModelChoiceField(queryset=Goal.objects.none())
    field_order = CreateGoal.field_order

    class Meta:
        fields = CreateGoal.Meta.fields + ["is_archived", "is_starred"]
        model = Goal

    def get_instance(self) -> Goal:
        return Goal.objects.get(user=self.user, pk=self.opts["pk"])

    def init(self):
        setup_datetime_field(self.fields["deadline"])

    def ok(self):
        self.instance.save()
        return self.instance.pk


class DeleteGoal(OptsUserInstance[Goal], forms.ModelForm):
    navs = ["goals"]
    text = "Are you sure you want to delete this goal?"
    submit = "Delete"

    class Meta:
        model = Goal
        fields = []

    def get_instance(self) -> Goal:
        return Goal.objects.get(user=self.user, pk=self.opts["pk"])

    def ok(self):
        self.instance.delete()
        return self.instance.pk
