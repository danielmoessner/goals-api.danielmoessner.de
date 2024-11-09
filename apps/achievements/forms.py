from django import forms
from apps.achievements.models import Achievement
from apps.todos.forms import OptsUserInstance
from apps.todos.utils import setup_date_field, setup_datetime_field


class CreateAchievement(OptsUserInstance[Achievement], forms.ModelForm):
    navs = ["achievements"]

    class Meta:
        model = Achievement
        fields = ["date", "title", "description"]

    def init(self):
        setup_date_field(self.fields["date"])

    def ok(self):
        self.instance.user = self.user
        self.instance.save()
        return self.instance.pk
