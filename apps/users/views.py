from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from apps.users.serializers import CreateUserSerializer, ChangePasswordSerializer
from apps.users.models import CustomUser
from django.shortcuts import redirect
from rest_framework import generics, status
from django.views import generic
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


class CreateUser(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SettingsView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'users/users_settings.j2'


class SignUpView(generic.TemplateView):
    template_name = 'users/users_sign_up.j2'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:redirect', permanent=False)
        return super(SignUpView, self).get(self, request, *args, **kwargs)


class SignInView(generic.TemplateView):
    template_name = 'users/users_sign_in.j2'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:redirect', permanent=False)
        return super(SignInView, self).get(self, request, *args, **kwargs)
