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


class CustomUserStarForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('goal_depth', 'goal_choice', 'progress_monitor_choice', 'link_choice', 'strategy_choice')


class CustomUserToDosForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('to_dos_delta', 'normal_to_dos_choice', 'repetitive_to_dos_choice', 'never_ending_to_dos_choice',
                  'multiple_to_dos_choice', 'pipeline_to_dos_choice')


class CustomUserPageForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('page_choice',)
