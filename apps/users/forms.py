from base64 import urlsafe_b64encode

from django import forms
from django.conf import settings
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
)
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes

from apps.users.generators import ChangeEmailTokenGenerator, ConfirmEmailTokenGenerator
from apps.users.models import CustomUser


class LoginForm(AuthenticationForm):
    submit = "Login"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "E-Mail"


class ChangePasswordForm(PasswordChangeForm):
    def send_mail(self, user: CustomUser):
        subject = "Dein Passwort wurde geändert"
        body = loader.render_to_string("users/change_password_3_email.txt", {})
        email_message = EmailMultiAlternatives(
            subject, body, settings.DEFAULT_FROM_EMAIL, [user.email]
        )
        html_email = loader.render_to_string("users/change_password_3_email.html", {})
        email_message.attach_alternative(html_email, "text/html")
        email_message.send()

    def save(self, commit=True):
        user = super().save(commit=commit)
        assert isinstance(user, CustomUser)
        if commit:
            self.send_mail(user)
        return user


class ChangeEmailForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["new_email"]

    def send_activation_mail(self, request, user):
        token = ChangeEmailTokenGenerator().make_token(user)
        current_site = get_current_site(request)
        uid = urlsafe_b64encode(force_bytes(user.pk)).decode()
        url = reverse_lazy(
            "change_email_confirm", kwargs={"uidb64": uid, "token": token}
        )
        protocol = "https" if request.is_secure() else "http"
        link = f"{protocol}://{current_site}{url}"
        subject = "Bestätige deine neue E-Mail-Adresse"

        context = {"link": link}
        body = loader.render_to_string("users/change_email_3_email_send.txt", context)

        email_message = EmailMultiAlternatives(
            subject, body, settings.DEFAULT_FROM_EMAIL, [user.new_email]
        )
        html_email = loader.render_to_string(
            "users/change_email_3_email_send.html", context
        )
        email_message.attach_alternative(html_email, "text/html")

        email_message.send()

    def save(self, commit=True, request=None):
        user: CustomUser = super().save(commit=False)
        if commit:
            user.save()
            try:
                self.send_activation_mail(request, user)
            except Exception as e:
                user.new_email = None
                user.save()
                raise e
        return user


class CustomUserCreationForm(UserCreationForm):
    submit = "Register"

    class Meta:
        model = CustomUser
        fields = ("email", "password1", "password2")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs = {"autocomplete": "email"}

    def send_activation_mail(self, request, user):
        token = ConfirmEmailTokenGenerator().make_token(user)
        current_site = get_current_site(request)
        uid = urlsafe_b64encode(force_bytes(user.pk)).decode()
        url = reverse_lazy(
            "register_confirm_email", kwargs={"uidb64": uid, "token": token}
        )
        protocol = "https" if request.is_secure() else "http"
        link = f"{protocol}://{current_site}{url}"
        subject = "Bestätige deine E-Mail-Adresse"

        context = {"link": link}
        body = loader.render_to_string("users/register_user_3_email_send.txt", context)
        email_message = EmailMultiAlternatives(
            subject, body, settings.DEFAULT_FROM_EMAIL, [user.email]
        )
        html_email = loader.render_to_string(
            "users/register_user_3_email_send.html", context
        )
        email_message.attach_alternative(html_email, "text/html")
        email_message.send()

    def save(self, commit=True, request=None):
        user: CustomUser = super().save(commit=False)
        if commit:
            user.save()
            try:
                self.send_activation_mail(request, user)
            except Exception as e:
                user.delete()
                raise e
        return user


class CustomPasswordResetForm(PasswordResetForm):
    text = "Please type in your email and we will send a password reset email."


class CustomSetPasswordForm(SetPasswordForm):
    pass
