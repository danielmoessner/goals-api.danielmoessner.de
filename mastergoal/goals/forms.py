from django import forms
from django.utils import timezone

from mastergoal.goals.models import ProgressMonitor
from mastergoal.goals.models import NeverEndingToDo
from mastergoal.goals.models import RepetitiveToDo
from mastergoal.goals.models import PipelineToDo
from mastergoal.goals.models import MultipleToDo
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
        fields = ('name', 'why', 'impact', 'deadline')

    def __init__(self, user, *args, **kwargs):
        super(GoalForm, self).__init__(*args, **kwargs)
        self.instance.user = user
        self.fields["deadline"].initial = timezone.now()

    def save(self, commit=True):
        super(GoalForm, self).save(commit=commit)
        if commit:
            self.instance.calc()
        return self.instance


# Milestone
class ProgressMonitorForm(forms.ModelForm):
    class Meta:
        model = ProgressMonitor
        fields = ('goal', 'monitor', 'weight', 'steps', 'notes')

    def __init__(self, user, *args, **kwargs):
        super(ProgressMonitorForm, self).__init__(*args, **kwargs)
        self.fields["goal"].queryset = user.goals.exclude(progress=100).order_by('name')

    def save(self, commit=True):
        super(ProgressMonitorForm, self).save(commit=commit)
        if commit:
            self.instance.calc()
        return self.instance


class ProgressMonitorStepForm(forms.ModelForm):
    class Meta:
        model = ProgressMonitor
        fields = ('step',)

    def __init__(self, user, *args, **kwargs):
        super(ProgressMonitorStepForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        super(ProgressMonitorStepForm, self).save(commit=commit)
        if commit:
            self.instance.calc()
        return self.instance


# Link
class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ('master_goal', 'sub_goal', 'weight', 'proportion')

    def __init__(self, user, *args, **kwargs):
        super(LinkForm, self).__init__(*args, **kwargs)
        self.fields["master_goal"].queryset = user.goals.exclude(progress=100).order_by('name')
        self.fields["sub_goal"].queryset = user.goals.exclude(progress=100).order_by('name')

    def save(self, commit=True):
        super(LinkForm, self).save(commit=commit)
        if commit:
            self.instance.calc()
        return self.instance


# Strategy
class StrategyForm(forms.ModelForm):
    deadline = forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        input_formats=["%Y-%m-%dT%H:%M"], label="Deadline (not required)", required=False)
    rolling = forms.DurationField(initial='7 days 00:00:00', required=False, label='Rolling (not required)')

    class Meta:
        model = Strategy
        fields = ('name', 'goal', 'description', 'deadline', 'weight', 'rolling')

    def __init__(self, user, *args, **kwargs):
        super(StrategyForm, self).__init__(*args, **kwargs)
        self.fields["goal"].queryset = user.goals.exclude(progress=100).order_by('name')
        self.fields["deadline"].initial = timezone.now()

    def save(self, commit=True):
        super(StrategyForm, self).save(commit=commit)
        if commit:
            self.instance.calc()
        return self.instance


# NormalToDo
class ToDoForm(forms.ModelForm):
    activate = forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        input_formats=["%Y-%m-%dT%H:%M"], label="Activate (not required)", required=False)
    deadline = forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        input_formats=["%Y-%m-%dT%H:%M"], label="Deadline (not required)", required=False)

    class Meta:
        model = ToDo
        fields = ('name', 'strategy', 'activate', 'deadline', 'notes')

    def __init__(self, user, *args, **kwargs):
        super(ToDoForm, self).__init__(*args, **kwargs)
        self.fields["strategy"].queryset = Strategy.objects.filter(goal__in=user.goals.exclude(progress=100))\
            .order_by('name')
        self.fields["deadline"].initial = timezone.now()
        self.fields["activate"].initial = timezone.now()

    def save(self, commit=True):
        super(ToDoForm, self).save(commit=commit)
        if commit:
            self.instance.calc()
        return self.instance


class ToDoDoneForm(forms.ModelForm):
    class Meta:
        model = ToDo
        fields = ("is_done",)

    def __init__(self, user, *args, **kwargs):
        super(ToDoDoneForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        super(ToDoDoneForm, self).save(commit=commit)
        if commit:
            self.instance.calc()
        return self.instance


class ToDoFailedForm(forms.ModelForm):
    class Meta:
        model = ToDo
        fields = ("has_failed",)

    def __init__(self, user, *args, **kwargs):
        super(ToDoFailedForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        super(ToDoFailedForm, self).save(commit=commit)
        if commit:
            self.instance.calc()
        return self.instance


class ToDoNotesForm(forms.ModelForm):
    class Meta:
        model = ToDo
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

    def save(self, commit=True):
        super(RepetitiveToDoForm, self).save(commit=commit)
        if commit:
            self.instance.calc()
        return self.instance


class RepetitiveToDoDoneForm(forms.ModelForm):
    class Meta:
        model = RepetitiveToDo
        fields = ("is_done",)

    def __init__(self, user, *args, **kwargs):
        super(RepetitiveToDoDoneForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        super(RepetitiveToDoDoneForm, self).save(commit=commit)
        if commit:
            self.instance.calc()
        return self.instance


class RepetitiveToDoFailedForm(forms.ModelForm):
    class Meta:
        model = RepetitiveToDo
        fields = ("has_failed",)

    def __init__(self, user, *args, **kwargs):
        super(RepetitiveToDoFailedForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        super(RepetitiveToDoFailedForm, self).save(commit=commit)
        if commit:
            self.instance.calc()
        return self.instance


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

    def save(self, commit=True):
        self.instance.deadline = timezone.now() + self.instance.duration
        super(NeverEndingToDoForm, self).save(commit=commit)
        if commit:
            self.instance.calc()
        return self.instance


class NeverEndingToDoDoneForm(forms.ModelForm):
    class Meta:
        model = NeverEndingToDo
        fields = ("is_done",)

    def __init__(self, user, *args, **kwargs):
        super(NeverEndingToDoDoneForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        super(NeverEndingToDoDoneForm, self).save(commit=commit)
        if commit:
            self.instance.calc()
        return self.instance


class NeverEndingToDoFailedForm(forms.ModelForm):
    class Meta:
        model = PipelineToDo
        fields = ("has_failed",)

    def __init__(self, user, *args, **kwargs):
        super(NeverEndingToDoFailedForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        super(NeverEndingToDoFailedForm, self).save(commit=commit)
        if commit:
            self.instance.calc()
        return self.instance


# NeverEndingToDo
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

    def save(self, commit=True):
        super(PipelineToDoForm, self).save(commit=commit)
        if commit:
            self.instance.calc()
        return self.instance


class PipelineToDoDoneForm(forms.ModelForm):
    class Meta:
        model = PipelineToDo
        fields = ("is_done",)

    def __init__(self, user, *args, **kwargs):
        super(PipelineToDoDoneForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        super(PipelineToDoDoneForm, self).save(commit=commit)
        if commit:
            self.instance.calc()
        return self.instance


class PipelineToDoFailedForm(forms.ModelForm):
    class Meta:
        model = NeverEndingToDo
        fields = ("has_failed",)

    def __init__(self, user, *args, **kwargs):
        super(PipelineToDoFailedForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        super(PipelineToDoFailedForm, self).save(commit=commit)
        if commit:
            self.instance.calc()
        return self.instance


# MultipleToDo
class MultipleToDoDoneForm(forms.ModelForm):
    class Meta:
        model = MultipleToDo
        fields = ("is_done",)

    def __init__(self, user, *args, **kwargs):
        super(MultipleToDoDoneForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        super(MultipleToDoDoneForm, self).save(commit=commit)
        if commit:
            self.instance.calc()
        return self.instance


class MultipleToDoFailedForm(forms.ModelForm):
    class Meta:
        model = MultipleToDo
        fields = ("has_failed",)

    def __init__(self, user, *args, **kwargs):
        super(MultipleToDoFailedForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        super(MultipleToDoFailedForm, self).save(commit=commit)
        if commit:
            self.instance.calc()
        return self.instance
