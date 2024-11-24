from typing import TYPE_CHECKING

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.users.generators import ChangeEmailTokenGenerator, ConfirmEmailTokenGenerator

if TYPE_CHECKING:
    from apps.story.models import Story


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    # make email the default login method
    username = None
    email = models.EmailField("E-Mail Address", unique=True)
    email_confirmed = models.BooleanField(default=False)
    new_email = models.EmailField("Neue E-Mail", blank=True, null=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()  # type: ignore
    # goals
    show_archived_objects = models.BooleanField(default=False)
    # todos
    show_old_todos = models.BooleanField(default=False)

    if TYPE_CHECKING:
        stories: models.QuerySet[Story]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def confirm_email_token(self, token: str):
        if self.email_confirmed:
            return
        if ConfirmEmailTokenGenerator().check_token(self, token):
            self.email_confirmed = True
            self.save()
        else:
            raise ValueError("token invalid")

    def confirm_new_email_token(self, token: str):
        if self.new_email is None:
            return
        if ChangeEmailTokenGenerator().check_token(self, token):
            self.email = self.new_email
            self.new_email = None
            self.save()
        else:
            raise ValueError("token invalid")
