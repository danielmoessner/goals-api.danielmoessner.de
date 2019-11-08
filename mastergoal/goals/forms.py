from django.utils import timezone
from django import forms

from mastergoal.goals.models import ProgressMonitor
from mastergoal.goals.models import NeverEndingToDo
from mastergoal.goals.models import RepetitiveToDo
from mastergoal.goals.models import PipelineToDo
from mastergoal.goals.models import MultipleToDo
from mastergoal.goals.models import NormalToDo
from mastergoal.goals.models import Strategy
from mastergoal.goals.models import Goal
from mastergoal.goals.models import ToDo
from mastergoal.goals.models import Link


# Goal
class GoalForm(forms.ModelForm):
    deadline = forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        input_formats=["%Y-%m-%dT%H:%M"], label="Deadline (not required)", required=False)

    class Meta:
        model = Goal
        fields = ('name', 'why', 'impact', 'deadline', 'is_archived', 'addition')

    def __init__(self, user, *args, **kwargs):
        super(GoalForm, self).__init__(*args, **kwargs)
        self.instance.user = user
        self.fields["deadline"].initial = timezone.now()


# Milestone
class ProgressMonitorForm(forms.ModelForm):
    class Meta:
        model = ProgressMonitor
        fields = ('goal', 'monitor', 'weight', 'steps', 'notes')

    def __init__(self, user, *args, **kwargs):
        super(ProgressMonitorForm, self).__init__(*args, **kwargs)
        self.fields["goal"].queryset = user.goals.exclude(progress=100).order_by('name')


class ProgressMonitorStepForm(forms.ModelForm):
    class Meta:
        model = ProgressMonitor
        fields = ('step',)

    def __init__(self, user, *args, **kwargs):
        super(ProgressMonitorStepForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['step'] > self.instance.steps:
            cleaned_data['step'] = self.instance.steps
        return cleaned_data


# Link
class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = '__all__'

    def __init__(self, user, *args, **kwargs):
        super(LinkForm, self).__init__(*args, **kwargs)
        self.fields["master_goal"].queryset = user.goals.exclude(progress=100).order_by('name')
        self.fields["sub_goal"].queryset = user.goals.exclude(progress=100).order_by('name')


# Strategy
class StrategyForm(forms.ModelForm):
    deadline = forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        input_formats=["%Y-%m-%dT%H:%M"], label="Deadline (not required)", required=False)
    rolling = forms.DurationField(initial='7 days 00:00:00', required=False, label='Rolling (not required)')

    class Meta:
        model = Strategy
        fields = '__all__'

    def __init__(self, user, *args, **kwargs):
        super(StrategyForm, self).__init__(*args, **kwargs)
        self.fields["goal"].queryset = user.goals.exclude(progress=100).order_by('name')
        self.fields["deadline"].initial = timezone.now()


# NormalToDo
class ToDoForm(forms.ModelForm):
    activate = forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        input_formats=["%Y-%m-%dT%H:%M"], label="Activate (not required)", required=False)
    deadline = forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        input_formats=["%Y-%m-%dT%H:%M"], label="Deadline (not required)", required=False)

    class Meta:
        model = NormalToDo
        fields = ('name', 'strategy', 'activate', 'deadline', 'notes')

    def __init__(self, user, *args, **kwargs):
        super(ToDoForm, self).__init__(*args, **kwargs)
        self.fields["strategy"].queryset = Strategy.objects.filter(goal__in=user.goals.exclude(progress=100))\
            .order_by('name')
        self.fields["deadline"].initial = timezone.now()
        self.fields["activate"].initial = timezone.now()


class ToDoDoneForm(forms.ModelForm):
    class Meta:
        model = NormalToDo
        fields = ("is_done",)

    def __init__(self, user, *args, **kwargs):
        super(ToDoDoneForm, self).__init__(*args, **kwargs)


class ToDoFailedForm(forms.ModelForm):
    class Meta:
        model = NormalToDo
        fields = ("has_failed",)

    def __init__(self, user, *args, **kwargs):
        super(ToDoFailedForm, self).__init__(*args, **kwargs)


class ToDoNotesForm(forms.ModelForm):
    class Meta:
        model = NormalToDo
        fields = ("notes",)

    def __init__(self, user, *args, **kwargs):
        super(ToDoNotesForm, self).__init__(*args, **kwargs)


# RepetitiveToDo
class RepetitiveToDoForm(forms.ModelForm):
    duration = forms.DurationField(initial='7 days 00:00:00')
    activate = forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        input_formats=["%Y-%m-%dT%H:%M"], label="Activate")
    deadline = forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        input_formats=["%Y-%m-%dT%H:%M"], label="Deadline")
    end_day = forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        input_formats=["%Y-%m-%dT%H:%M"], label="End Day")

    class Meta:
        model = RepetitiveToDo
        fields = ('name', 'strategy', 'activate', 'deadline', 'duration', 'end_day', 'notes')

    def __init__(self, user, *args, **kwargs):
        super(RepetitiveToDoForm, self).__init__(*args, **kwargs)
        self.fields["strategy"].queryset = Strategy.objects.filter(goal__in=user.goals.all()).order_by('name')
        self.fields["deadline"].initial = timezone.now()
        self.fields["activate"].initial = timezone.now()
        self.fields["end_day"].initial = timezone.now()


class RepetitiveToDoDoneForm(forms.ModelForm):
    class Meta:
        model = RepetitiveToDo
        fields = ("is_done",)

    def __init__(self, user, *args, **kwargs):
        super(RepetitiveToDoDoneForm, self).__init__(*args, **kwargs)


class RepetitiveToDoFailedForm(forms.ModelForm):
    class Meta:
        model = RepetitiveToDo
        fields = ("has_failed",)

    def __init__(self, user, *args, **kwargs):
        super(RepetitiveToDoFailedForm, self).__init__(*args, **kwargs)


# NeverEndingToDo
class NeverEndingToDoForm(forms.ModelForm):
    activate = forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        input_formats=["%Y-%m-%dT%H:%M"], label="Activate")
    duration = forms.DurationField(initial='0 days 00:00:00')

    class Meta:
        model = NeverEndingToDo
        fields = ('name', 'strategy', 'activate', 'duration', 'notes')

    def __init__(self, user, *args, **kwargs):
        super(NeverEndingToDoForm, self).__init__(*args, **kwargs)
        self.fields["strategy"].queryset = Strategy.objects.filter(goal__in=user.goals.all()).order_by('name')


class NeverEndingToDoDoneForm(forms.ModelForm):
    class Meta:
        model = NeverEndingToDo
        fields = ("is_done",)

    def __init__(self, user, *args, **kwargs):
        super(NeverEndingToDoDoneForm, self).__init__(*args, **kwargs)


class NeverEndingToDoFailedForm(forms.ModelForm):
    class Meta:
        model = NeverEndingToDo
        fields = ("has_failed",)

    def __init__(self, user, *args, **kwargs):
        super(NeverEndingToDoFailedForm, self).__init__(*args, **kwargs)


# PipelineToDo
class PipelineToDoForm(forms.ModelForm):
    deadline = forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        input_formats=["%Y-%m-%dT%H:%M"], label="Deadline (not required)", required=False)

    class Meta:
        model = PipelineToDo
        fields = ('name', 'strategy', 'deadline', 'previous', 'notes')

    def __init__(self, user, *args, **kwargs):
        super(PipelineToDoForm, self).__init__(*args, **kwargs)
        self.fields["strategy"].queryset = Strategy.objects.filter(goal__in=user.goals.all())
        self.fields["previous"].queryset = ToDo.objects.filter(strategy__in=Strategy.objects.filter(
            goal__in=user.goals.exclude(progress=100)), has_failed=False, is_done=False).order_by('name')
        self.fields["deadline"].initial = timezone.now()


class PipelineToDoDoneForm(forms.ModelForm):
    class Meta:
        model = PipelineToDo
        fields = ("is_done",)

    def __init__(self, user, *args, **kwargs):
        super(PipelineToDoDoneForm, self).__init__(*args, **kwargs)


class PipelineToDoFailedForm(forms.ModelForm):
    class Meta:
        model = PipelineToDo
        fields = ("has_failed",)

    def __init__(self, user, *args, **kwargs):
        super(PipelineToDoFailedForm, self).__init__(*args, **kwargs)


# MultipleToDo
class MultipleToDoDoneForm(forms.ModelForm):
    class Meta:
        model = MultipleToDo
        fields = ("is_done",)

    def __init__(self, user, *args, **kwargs):
        super(MultipleToDoDoneForm, self).__init__(*args, **kwargs)


class MultipleToDoFailedForm(forms.ModelForm):
    class Meta:
        model = MultipleToDo
        fields = ("has_failed",)

    def __init__(self, user, *args, **kwargs):
        super(MultipleToDoFailedForm, self).__init__(*args, **kwargs)
