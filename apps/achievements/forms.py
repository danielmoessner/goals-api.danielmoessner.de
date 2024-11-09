from django import forms
from apps.achievements.models import Achievement
from apps.todos.forms import OptsUserInstance


class CreateAchievement(OptsUserInstance[Achievement], forms.ModelForm):
    class Meta:
        model = Achievement
        fields = "__all__"

    def ok(self):
        self.instance.save()
        return self.instance.pk
