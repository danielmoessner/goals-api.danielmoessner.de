from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.core.exceptions import ImproperlyConfigured
from django.template.loader import render_to_string
from django.contrib.auth import login as auth_login
from django.views import generic
from django.http import HttpResponse
from django.urls import reverse_lazy

from apps.users.models import CustomUser
from apps.users.forms import UserStrategyMainChoiceForm
from apps.users.forms import CustomUserCreationForm
from apps.users.forms import CustomUserTreeViewForm
from apps.users.forms import CustomUserGoalViewForm
from apps.users.forms import CustomUserChangeForm
from apps.users.forms import CustomUserToDosForm
from apps.users.forms import CustomUserPageForm
from apps.core.views import CustomAjaxFormMixin

import json


class SignOutView(LogoutView):
    pass


class CustomUserSignIn(LoginView):
    template_name = 'snippets/form.j2'
    redirect_url = reverse_lazy('core:redirect')

    def get_redirect_url(self):
        if not self.redirect_url:
            raise ImproperlyConfigured("No URL to redirect to. Provide a redirect_url.")
        return str(self.redirect_url)

    def form_invalid(self, form):
        html = render_to_string(self.template_name, self.get_context_data(form=form),
                                request=self.request)
        return HttpResponse(json.dumps({"valid": False, "html": html}),
                            content_type="application/json")

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        return HttpResponse(json.dumps({"valid": True}), content_type="application/json")


class CustomUserSignUp(generic.CreateView):
    template_name = 'snippets/form.j2'
    success_url = reverse_lazy('users:sign_in')
    form_class = CustomUserCreationForm

    def form_invalid(self, form):
        html = render_to_string(self.template_name, self.get_context_data(form=form),
                                request=self.request)
        return HttpResponse(json.dumps({"valid": False, "html": html}),
                            content_type="application/json")

    def form_valid(self, form):
        user = form.save()
        auth_login(self.request, user)
        return HttpResponse(json.dumps({"valid": True}), content_type="application/json")


class CustomUserEdit(LoginRequiredMixin, UserPassesTestMixin, CustomAjaxFormMixin, generic.UpdateView):
    form_class = CustomUserChangeForm
    template_name = 'snippets/form.j2'
    model = CustomUser

    def test_func(self):
        if self.get_object() == self.request.user:
            return True
        return False


class CustomUserPassword(LoginRequiredMixin, CustomAjaxFormMixin, PasswordChangeView):
    template_name = 'snippets/form.j2'
    success_url = 'users:sign_in'


class CustomUserTreeViewChoices(LoginRequiredMixin, UserPassesTestMixin, CustomAjaxFormMixin, generic.UpdateView):
    form_class = CustomUserTreeViewForm
    template_name = 'snippets/form.j2'
    model = CustomUser

    def test_func(self):
        if self.get_object() == self.request.user:
            return True
        return False


class CustomUserGoalViewChoices(LoginRequiredMixin, UserPassesTestMixin, CustomAjaxFormMixin, generic.UpdateView):
    form_class = CustomUserGoalViewForm
    template_name = 'snippets/form.j2'
    model = CustomUser

    def test_func(self):
        if self.get_object() == self.request.user:
            return True
        return False


class CustomUserToDosChoices(LoginRequiredMixin, UserPassesTestMixin, CustomAjaxFormMixin, generic.UpdateView):
    form_class = CustomUserToDosForm
    template_name = 'snippets/form.j2'
    model = CustomUser

    def test_func(self):
        if self.get_object() == self.request.user:
            return True
        return False


class CustomUserPageChoice(LoginRequiredMixin, UserPassesTestMixin, CustomAjaxFormMixin, generic.UpdateView):
    form_class = CustomUserPageForm
    template_name = 'snippets/form.j2'
    model = CustomUser

    def test_func(self):
        if self.get_object() == self.request.user:
            return True
        return False


class UpdateStrategyMainChoicesUser(LoginRequiredMixin, UserPassesTestMixin, CustomAjaxFormMixin, generic.UpdateView):
    form_class = UserStrategyMainChoiceForm
    template_name = 'snippets/form.j2'
    model = CustomUser

    def test_func(self):
        if self.get_object() == self.request.user:
            return True
        return False
