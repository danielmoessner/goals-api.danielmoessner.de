from django import forms

from apps.achievements.models import Achievement
from apps.todos.forms import OptsUserInstance
from apps.todos.utils import setup_date_field


class CreateAchievement(OptsUserInstance[Achievement], forms.ModelForm):
    navs = ["achievements"]
    submit = "Create"

    class Meta:
        model = Achievement
        fields = ["date", "title", "description"]

    def init(self):
        setup_date_field(self.fields["date"])

    def ok(self):
        self.instance.user = self.user
        self.instance.save()
        return self.instance.pk


class UpdateAchievement(OptsUserInstance[Achievement], forms.ModelForm):
    navs = ["achievements"]

    class Meta:
        model = Achievement
        fields = CreateAchievement.Meta.fields

    def init(self):
        setup_date_field(self.fields["date"])

    def get_instance(self):
        return Achievement.objects.get(pk=self.opts["pk"], user=self.user)

    def ok(self):
        self.instance.save()
        return self.instance.pk


class DeleteAchievement(OptsUserInstance[Achievement], forms.ModelForm):
    navs = ["achievements"]
    text = "Are you sure you want to delete this achievement?"
    submit = "Delete"

    class Meta:
        model = Achievement
        fields = []

    def get_instance(self):
        return Achievement.objects.get(pk=self.opts["pk"], user=self.user)

    def ok(self):
        self.instance.delete()
        return self.instance.pk
