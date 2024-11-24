import logging
from base64 import urlsafe_b64decode

from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.contrib.auth.views import (
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
)
from django.core.exceptions import ValidationError
from django.views.generic import TemplateView

from apps.users.models import CustomUser

logger = logging.getLogger(__name__)


class LogoutView(DjangoLogoutView):
    pass


class ChangePasswordDoneView(TemplateView):
    template_name = "users/change_password_done.html"


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


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "users/password_reset_2_done.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "users/password_reset_3_confirm.html"


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "users/password_reset_4_complete.html"
