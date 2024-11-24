import logging
from base64 import urlsafe_b64decode

from django.conf import settings
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.core.exceptions import PermissionDenied, ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from apps.users.forms import (
    ChangeEmailForm,
    ChangePasswordForm,
    CustomUserCreationForm,
    LoginForm,
)
from apps.users.models import CustomUser

logger = logging.getLogger(__name__)


# login
class LoginView(DjangoLoginView):
    template_name = "users/login.html"
    redirect_authenticated_user = True
    redirect_field_name = "next"
    form_class = LoginForm


class LogoutView(DjangoLogoutView):
    pass


# change passwort
class ChangePasswordView(PasswordChangeView):
    form_class = ChangePasswordForm
    success_url = reverse_lazy("change_password_done")
    template_name = "users/change_password.html"


class ChangePasswordDoneView(TemplateView):
    template_name = "users/change_password_done.html"


# change email
class ChangeEmailView(FormView):
    form_class = ChangeEmailForm
    template_name = "users/change_email_1_form.html"
    success_url = reverse_lazy("change_email_done")
    template_name = "users/change_email_1_form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"instance": self.request.user})
        return kwargs

    def form_valid(self, form):
        form.save(request=self.request)
        return HttpResponseRedirect(self.get_success_url())


class ChangeEmailDoneView(TemplateView):
    template_name = "users/change_email_2_done.html"


class ChangeEmailConfirmView(TemplateView):
    template_name = "users/change_email_4_success.html"

    def get(self, request, *args, **kwargs):
        user = self.get_user(kwargs["uidb64"])
        if user is not None:
            try:
                user.confirm_new_email_token(kwargs["token"])
            except ValueError:
                return self.render_to_response({"validlink": False})
            return self.render_to_response({"validlink": True})
        else:
            return self.render_to_response({"validlink": False})

    def get_user(self, uidb64):
        try:
            uid = urlsafe_b64decode(uidb64).decode()
            user = CustomUser.objects.get(pk=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            CustomUser.DoesNotExist,
            ValidationError,
        ):
            user = None
        return user


# register
class CustomRegisterView(FormView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("register_user_done")
    template_name = "users/register_user_1.html"

    def post(self, request, *args, **kwargs):
        if not settings.CUSTOM_ALLOW_REGISTRATION:
            raise PermissionDenied()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.save(request=self.request)
        return HttpResponseRedirect(self.get_success_url())


class CustomRegisterDoneView(TemplateView):
    template_name = "users/register_user_2_done.html"


class CustomRegisterConfirmEmailView(TemplateView):
    template_name = "users/register_user_4_email_confirmed.html"

    def get(self, request, *args, **kwargs):
        user = self.get_user(kwargs["uidb64"])
        if user is not None:
            try:
                user.confirm_email_token(kwargs["token"])
            except ValueError:
                return self.render_to_response({"validlink": False})
            return self.render_to_response({"validlink": True})
        else:
            return self.render_to_response({"validlink": False})

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_b64decode(uidb64).decode()
            user = CustomUser.objects.get(pk=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            CustomUser.DoesNotExist,
            ValidationError,
        ):
            user = None
        return user


# password forgotten
class CustomPasswordResetView(PasswordResetView):
    template_name = "users/password_reset_1_form.html"
    # form_class = CustomPasswordResetForm


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "users/password_reset_2_done.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "users/password_reset_3_confirm.html"


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "users/password_reset_4_complete.html"
