from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email')


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class CustomUserPasswordForm(PasswordChangeForm):
    class Meta:
        model = CustomUser


class CustomUserStarHeaderForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('goal_choice', 'progress_monitor_choice', 'link_choice', 'strategy_choice')
        labels = {
            'goal_choice': 'Goals',
            'progress_monitor_choice': 'Progress Monitor',
            'link_choice': 'Links',
            'strategy_choice': 'Strategies',
            'to_do_choice': "To Do's"
        }


class CustomUserGoalViewForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('goal_view_goal_choice',)


class CustomUserStarForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('goal_depth', 'goal_choice', 'progress_monitor_choice', 'link_choice', 'strategy_choice',
                  'starview_normaltodos_choice', 'starview_neverendingtodos_choice', 'starview_repetitivetodos_choice',
                  'starview_pipelinetodos_choice')


class CustomUserTreeViewForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('treeview_goal_depth', 'treeview_goal_choice', 'treeview_monitor_choice',
                  'treeview_strategy_choice', 'treeview_todos_delta',
                  'treeview_normaltodos_choice', 'treeview_repetitivetodos_choice', 'treeview_neverendingtodos_choice',
                  'treeview_pipelinetodos_choice')


class CustomUserToDosForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('to_dos_delta', 'normal_to_dos_choice', 'repetitive_to_dos_choice', 'never_ending_to_dos_choice',
                  'pipeline_to_dos_choice')


class CustomUserPageForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('page_choice', 'show_archived_objects')
