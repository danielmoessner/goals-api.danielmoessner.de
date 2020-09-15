from apps.goals.models import ProgressMonitor, Strategy, Goal, Link
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
