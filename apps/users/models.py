from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # make email the default login method
    username = None
    email = models.EmailField('E-Mail Address', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    # goals
    show_archived_objects = models.BooleanField(default=False)
    # todos
    show_old_todos = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
