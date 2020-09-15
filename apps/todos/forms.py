from apps.todos.models import NeverEndingToDo, RepetitiveToDo, PipelineToDo, NormalToDo, ToDo
from apps.todos.utils import get_todo_in_its_proper_class
from django.utils import timezone
from django import forms


###
# ParentToDo: Done, Status, Notes, Archived
###
# class ToDoDoneForm(forms.ModelForm):
#     class Meta:
#         model = ToDo
#         fields = ("status",)
#
#     def save(self, commit=True):
#         new_instance = get_todo_in_its_proper_class(self.instance.pk)
#         new_instance.is_done = self.instance.is_done
#         self.instance = new_instance
#         return super().save(commit=commit)
#
#
# class ToDoStatusForm(forms.ModelForm):
#     class Meta:
#         model = ToDo
#         fields = ("status",)
#
#     def save(self, commit=True):
#         new_instance = get_todo_in_its_proper_class(self.instance.pk)
#         new_instance.status = self.instance.status
#         self.instance = new_instance
#         return super().save(commit=commit)
#
#
# class ToDoIsArchivedForm(forms.ModelForm):
#     class Meta:
#         model = ToDo
#         fields = ("is_archived",)
#
#     def save(self, commit=True):
#         new_instance = get_todo_in_its_proper_class(self.instance.pk)
#         new_instance.is_archived = self.instance.is_archived
#         self.instance = new_instance
#         return super().save(commit=commit)
#
#
# ###
# # NormalToDo
# ###
# class NormalToDoForm(forms.ModelForm):
#     activate = forms.DateTimeField(widget=forms.DateTimeInput(
#         attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
#         input_formats=["%Y-%m-%dT%H:%M"], label="Activate (not required)", required=False)
#     deadline = forms.DateTimeField(widget=forms.DateTimeInput(
#         attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
#         input_formats=["%Y-%m-%dT%H:%M"], label="Deadline (not required)", required=False)
#
#     class Meta:
#         model = NormalToDo
#         fields = ('name', 'activate', 'deadline', 'notes', 'is_archived')
#         fieldsets = (
#             (None, {
#                 'fields': ('name', 'strategy')
#             }),
#             ('Additional Options', {
#                 'fields': ('activate', 'deadline', 'notes'),
#                 'classes': ('collapse',)
#             }),
#             ('Advanced Options', {
#                 'fields': ('is_archived'),
#                 'classes': ('collapse',)
#             })
#         )
#
#     def __init__(self, user, *args, **kwargs):
#         super(NormalToDoForm, self).__init__(*args, **kwargs)
#         self.instance.user = user
#
#
# class NormalToDoDoneForm(forms.ModelForm):
#     class Meta:
#         model = NormalToDo
#         fields = ("status",)
#
#     def __init__(self, user, *args, **kwargs):
#         super(NormalToDoDoneForm, self).__init__(*args, **kwargs)
#
#
# class NormalToDoFailedForm(forms.ModelForm):
#     class Meta:
#         model = NormalToDo
#         fields = ("status",)
#
#     def __init__(self, user, *args, **kwargs):
#         super(NormalToDoFailedForm, self).__init__(*args, **kwargs)
#
#
# class ToDoNotesForm(forms.ModelForm):
#     class Meta:
#         model = ToDo
#         fields = ("notes",)
#
#     def __init__(self, user, *args, **kwargs):
#         super(ToDoNotesForm, self).__init__(*args, **kwargs)
#
#
# # RepetitiveToDo
# class RepetitiveToDoForm(forms.ModelForm):
#     duration = forms.DurationField(initial='7 days 00:00:00')
#     activate = forms.DateTimeField(widget=forms.DateTimeInput(
#         attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
#         input_formats=["%Y-%m-%dT%H:%M"], label="Activate")
#     deadline = forms.DateTimeField(widget=forms.DateTimeInput(
#         attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
#         input_formats=["%Y-%m-%dT%H:%M"], label="Deadline", required=False)
#
#     class Meta:
#         model = RepetitiveToDo
#         fields = (
#             'name', 'activate', 'duration', 'deadline', 'repetitions', 'notes', 'is_archived', 'is_done',
#             'has_failed', 'previous'
#         )
#         fieldsets = (
#             (None, {
#                 'fields': ('name', 'activate', 'duration', 'repetitions')
#             }),
#             ('Additional Options', {
#                 'fields': ('notes',),
#                 'classes': ('collapse',)
#             }),
#             ('Advanced Options', {
#                 'fields': ('deadline', 'is_archived', 'is_done', 'has_failed', 'previous'),
#                 'classes': ('collapse',)
#             })
#         )
#
#     def __init__(self, user, *args, **kwargs):
#         super(RepetitiveToDoForm, self).__init__(*args, **kwargs)
#         self.instance.user = user
#         self.fields["activate"].initial = timezone.now()
#
#     def clean(self):
#         cleaned_data = super().clean()
#         deadline = cleaned_data['deadline']
#         if deadline is None:
#             deadline = cleaned_data['activate'] + cleaned_data['duration']
#             cleaned_data['deadline'] = deadline
#         return cleaned_data
#
#
# class RepetitiveToDoDoneForm(forms.ModelForm):
#     class Meta:
#         model = RepetitiveToDo
#         fields = ("status",)
#
#     def __init__(self, user, *args, **kwargs):
#         super(RepetitiveToDoDoneForm, self).__init__(*args, **kwargs)
#
#
# class RepetitiveToDoFailedForm(forms.ModelForm):
#     class Meta:
#         model = RepetitiveToDo
#         fields = ("status",)
#
#     def __init__(self, user, *args, **kwargs):
#         super(RepetitiveToDoFailedForm, self).__init__(*args, **kwargs)
#
#
# # NeverEndingToDo
# class NeverEndingToDoForm(forms.ModelForm):
#     activate = forms.DateTimeField(widget=forms.DateTimeInput(
#         attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
#         input_formats=["%Y-%m-%dT%H:%M"], label="Activate")
#     duration = forms.DurationField(initial='0 days 00:00:00')
#     deadline = forms.DateTimeField(widget=forms.DateTimeInput(
#         attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
#         input_formats=["%Y-%m-%dT%H:%M"], label="Deadline", required=False)
#
#     class Meta:
#         model = NeverEndingToDo
#         fields = (
#             'name', 'duration', 'activate', 'deadline', 'notes', 'is_archived', 'is_done', 'has_failed'
#         )
#         fieldsets = (
#             (None, {
#                 'fields': ('name', 'duration')
#             }),
#             ('Additional Options', {
#                 'fields': ('notes',),
#                 'classes': ('collapse',)
#             }),
#             ('Advanced Options', {
#                 'fields': ('deadline', 'is_archived', 'is_done', 'has_failed', 'activate'),
#                 'classes': ('collapse',)
#             })
#         )
#
#     def __init__(self, user, *args, **kwargs):
#         super(NeverEndingToDoForm, self).__init__(*args, **kwargs)
#         self.instance.user = user
#         self.fields["activate"].initial = timezone.now()
#
#     def clean(self):
#         cleaned_data = super().clean()
#         deadline = cleaned_data['deadline']
#         if deadline is None:
#             deadline = cleaned_data['activate'] + cleaned_data['duration']
#             cleaned_data['deadline'] = deadline
#         return cleaned_data
#
#
# class NeverEndingToDoDoneForm(forms.ModelForm):
#     class Meta:
#         model = NeverEndingToDo
#         fields = ("status",)
#
#     def __init__(self, user, *args, **kwargs):
#         super(NeverEndingToDoDoneForm, self).__init__(*args, **kwargs)
#
#
# class NeverEndingToDoFailedForm(forms.ModelForm):
#     class Meta:
#         model = NeverEndingToDo
#         fields = ("status",)
#
#     def __init__(self, user, *args, **kwargs):
#         super(NeverEndingToDoFailedForm, self).__init__(*args, **kwargs)
#
#
# # PipelineToDo
# class PipelineToDoForm(forms.ModelForm):
#     deadline = forms.DateTimeField(widget=forms.DateTimeInput(
#         attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
#         input_formats=["%Y-%m-%dT%H:%M"], label="Deadline", required=False)
#     activate = forms.DateTimeField(widget=forms.DateTimeInput(
#         attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
#         input_formats=["%Y-%m-%dT%H:%M"], label="Activate", required=False)
#
#     class Meta:
#         model = PipelineToDo
#         fields = (
#             'name', 'previous', 'deadline', 'notes', 'is_archived', 'is_done', 'has_failed', 'activate'
#         )
#         fieldsets = (
#             (None, {
#                 'fields': ('name', 'previous')
#             }),
#             ('Additional Options', {
#                 'fields': ('notes',),
#                 'classes': ('collapse',)
#             }),
#             ('Advanced Options', {
#                 'fields': ('deadline', 'is_archived', 'is_done', 'has_failed', 'activate'),
#                 'classes': ('collapse',)
#             })
#         )
#
#     def __init__(self, user, *args, **kwargs):
#         super(PipelineToDoForm, self).__init__(*args, **kwargs)
#         self.instance.user = user
#         self.fields['strategy'].required = False
#         self.fields["previous"].queryset = ToDo.objects.filter(
#             user=user,
#             has_failed=False,
#             is_done=False
#         ).order_by('name')
#
#     def clean(self):
#         cleaned_data = super().clean()
#         strategy = cleaned_data['strategy']
#         if strategy is None:
#             previous = cleaned_data['previous']
#             strategy = previous.strategy
#             cleaned_data['strategy'] = strategy
#         return cleaned_data
#
#
# class PipelineToDoDoneForm(forms.ModelForm):
#     class Meta:
#         model = PipelineToDo
#         fields = ("status",)
#
#     def __init__(self, user, *args, **kwargs):
#         super(PipelineToDoDoneForm, self).__init__(*args, **kwargs)
#
#
# class PipelineToDoFailedForm(forms.ModelForm):
#     class Meta:
#         model = PipelineToDo
#         fields = ("status",)
#
#     def __init__(self, user, *args, **kwargs):
#         super(PipelineToDoFailedForm, self).__init__(*args, **kwargs)
