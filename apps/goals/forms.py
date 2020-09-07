from apps.goals.models import ProgressMonitor, NeverEndingToDo, RepetitiveToDo, PipelineToDo, Strategy, \
    NormalToDo, Goal, ToDo, Link
from django.utils import timezone
from django import forms


# Goal
class GoalForm(forms.ModelForm):
    deadline = forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        input_formats=["%Y-%m-%dT%H:%M"], label="Deadline (not required)", required=False)

    class Meta:
        model = Goal
        fields = ('name', 'why', 'impact', 'addition', 'deadline', 'is_archived', 'progress', 'is_starred')
        fieldsets = (
            (None, {
                'fields': ('name', 'why', 'impact')
            }),
            ('Additional Options', {
                'fields': ('deadline', 'addition'),
                'classes': ('collapse',)
            }),
            ('Advanced Options', {
                'fields': ('is_archived', 'progress', 'is_starred'),
                'classes': ('collapse',)
            })
        )

    def __init__(self, user, *args, **kwargs):
        super(GoalForm, self).__init__(*args, **kwargs)
        self.instance.user = user
        # self.fields["deadline"].initial = timezone.now()


# Milestone
class ProgressMonitorForm(forms.ModelForm):
    class Meta:
        model = ProgressMonitor
        fields = ('goal', 'monitor', 'steps', 'weight', 'notes', 'step', 'is_archived', 'progress')
        fieldsets = (
            (None, {
                'fields': ('goal', 'monitor', 'steps')
            }),
            ('Additional Options', {
                'fields': ('weight', 'notes'),
                'classes': ('collapse',)
            }),
            ('Advanced Options', {
                'fields': ('step', 'is_archived', 'progress'),
                'classes': ('collapse',)
            })
        )

    def __init__(self, user, *args, **kwargs):
        super(ProgressMonitorForm, self).__init__(*args, **kwargs)
        self.fields["goal"].queryset = user.goals.filter(is_archived=False).order_by('name')


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
        fieldsets = (
            (None, {
                'fields': ('master_goal', 'sub_goal')
            }),
            ('Additional Options', {
                'fields': ('weight', 'proportion'),
                'classes': ('collapse',)
            }),
            ('Advanced Options', {
                'fields': ('is_archived', 'progress'),
                'classes': ('collapse',)
            })
        )

    def __init__(self, user, *args, **kwargs):
        super(LinkForm, self).__init__(*args, **kwargs)
        self.fields["master_goal"].queryset = user.goals.filter(is_archived=False).order_by('name')
        self.fields["sub_goal"].queryset = user.goals.filter(is_archived=False).order_by('name')


# Strategy
class StrategyForm(forms.ModelForm):
    deadline = forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        input_formats=["%Y-%m-%dT%H:%M"], label="Deadline (not required)", required=False)
    rolling = forms.DurationField(required=False, label='Rolling (not required)', help_text='Example: 7 days 00:00:00')

    class Meta:
        model = Strategy
        fields = '__all__'
        fieldsets = (
            (None, {
                'fields': ('name', 'goal', 'description')
            }),
            ('Additional Options', {
                'fields': ('weight', 'rolling'),
                'classes': ('collapse',)
            }),
            ('Advanced Options', {
                'fields': ('is_archived', 'progress', 'is_starred'),
                'classes': ('collapse',)
            })
        )

    def __init__(self, user, *args, **kwargs):
        super(StrategyForm, self).__init__(*args, **kwargs)
        self.fields["goal"].queryset = user.goals.filter(is_archived=False).order_by('name')
        # self.fields["deadline"].initial = timezone.now()


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
        fields = ('name', 'strategy', 'activate', 'deadline', 'notes', 'is_archived', 'is_done', 'has_failed')
        fieldsets = (
            (None, {
                'fields': ('name', 'strategy')
            }),
            ('Additional Options', {
                'fields': ('activate', 'deadline', 'notes'),
                'classes': ('collapse',)
            }),
            ('Advanced Options', {
                'fields': ('is_archived', 'is_done', 'has_failed'),
                'classes': ('collapse',)
            })
        )

    def __init__(self, user, *args, **kwargs):
        super(ToDoForm, self).__init__(*args, **kwargs)
        self.fields["strategy"].queryset = Strategy.objects.filter(
            goal__in=user.goals.filter(is_archived=False),
            is_archived=False
        ).order_by('name')
        # self.fields["deadline"].initial = timezone.now()
        # self.fields["activate"].initial = timezone.now()


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
        input_formats=["%Y-%m-%dT%H:%M"], label="Deadline", required=False)

    class Meta:
        model = RepetitiveToDo
        fields = (
            'name', 'strategy', 'activate', 'duration', 'deadline', 'repetitions', 'notes', 'is_archived', 'is_done',
            'has_failed', 'previous'
        )
        fieldsets = (
            (None, {
                'fields': ('name', 'strategy', 'activate', 'duration', 'repetitions')
            }),
            ('Additional Options', {
                'fields': ('notes',),
                'classes': ('collapse',)
            }),
            ('Advanced Options', {
                'fields': ('deadline', 'is_archived', 'is_done', 'has_failed', 'previous'),
                'classes': ('collapse',)
            })
        )

    def __init__(self, user, *args, **kwargs):
        super(RepetitiveToDoForm, self).__init__(*args, **kwargs)
        self.fields["strategy"].queryset = Strategy.objects.filter(
            goal__in=user.goals.filter(is_archived=False),
            is_archived=False
        ).order_by('name')
        self.fields["activate"].initial = timezone.now()

    def clean(self):
        cleaned_data = super().clean()
        deadline = cleaned_data['deadline']
        if deadline is None:
            deadline = cleaned_data['activate'] + cleaned_data['duration']
            cleaned_data['deadline'] = deadline
        return cleaned_data


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
    deadline = forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        input_formats=["%Y-%m-%dT%H:%M"], label="Deadline", required=False)

    class Meta:
        model = NeverEndingToDo
        fields = (
            'name', 'strategy', 'duration', 'activate', 'deadline', 'notes', 'is_archived', 'is_done', 'has_failed'
        )
        fieldsets = (
            (None, {
                'fields': ('name', 'strategy', 'duration')
            }),
            ('Additional Options', {
                'fields': ('notes',),
                'classes': ('collapse',)
            }),
            ('Advanced Options', {
                'fields': ('deadline', 'is_archived', 'is_done', 'has_failed', 'activate'),
                'classes': ('collapse',)
            })
        )

    def __init__(self, user, *args, **kwargs):
        super(NeverEndingToDoForm, self).__init__(*args, **kwargs)
        self.fields["strategy"].queryset = Strategy.objects.filter(
            goal__in=user.goals.filter(is_archived=False),
            is_archived=False
        ).order_by('name')
        self.fields["activate"].initial = timezone.now()

    def clean(self):
        cleaned_data = super().clean()
        deadline = cleaned_data['deadline']
        if deadline is None:
            deadline = cleaned_data['activate'] + cleaned_data['duration']
            cleaned_data['deadline'] = deadline
        return cleaned_data


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
        input_formats=["%Y-%m-%dT%H:%M"], label="Deadline", required=False)
    activate = forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        input_formats=["%Y-%m-%dT%H:%M"], label="Activate", required=False)

    class Meta:
        model = PipelineToDo
        fields = (
            'name', 'strategy', 'previous', 'deadline', 'notes', 'is_archived', 'is_done', 'has_failed', 'activate'
                  )
        fieldsets = (
            (None, {
                'fields': ('name', 'previous')
            }),
            ('Additional Options', {
                'fields': ('strategy', 'notes'),
                'classes': ('collapse',)
            }),
            ('Advanced Options', {
                'fields': ('deadline', 'is_archived', 'is_done', 'has_failed', 'activate'),
                'classes': ('collapse',)
            })
        )

    def __init__(self, user, *args, **kwargs):
        super(PipelineToDoForm, self).__init__(*args, **kwargs)
        self.fields["strategy"].queryset = Strategy.objects.filter(
            goal__in=user.goals.filter(is_archived=False),
            is_archived=False
        ).order_by('name')
        self.fields['strategy'].required = False
        self.fields["previous"].queryset = ToDo.objects.filter(
            strategy__in=Strategy.objects.filter(
                goal__in=user.goals.filter(is_archived=False),
                is_archived=False
            ),
            has_failed=False,
            is_done=False
        ).order_by('name')

    def clean(self):
        cleaned_data = super().clean()
        strategy = cleaned_data['strategy']
        if strategy is None:
            previous = cleaned_data['previous']
            strategy = previous.strategy
            cleaned_data['strategy'] = strategy
        return cleaned_data


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
