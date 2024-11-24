from typing import Any, Generic, TypeVar

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
from django.db import models

from apps.users.models import CustomUser

USER = AbstractBaseUser | AnonymousUser | CustomUser
OPTS = dict[str, Any]
T = TypeVar("T", bound=models.Model)


class OptsUser:
    def init(self):
        pass

    def __init__(self, user: USER, opts: OPTS, *args, **kwargs):
        self.user = user
        self.opts = opts
        super().__init__(*args, **kwargs)  # type: ignore
        self.init()


class OptsUserInstance(Generic[T]):
    instance: T

    def init(self):
        pass

    def get_instance(self) -> models.Model | None:
        return None

    def __init__(self, user: USER, opts: OPTS, *args, **kwargs):
        assert isinstance(user, CustomUser)
        self.user = user
        self.opts = opts
        instance = self.get_instance()
        super().__init__(*args, instance=instance, **kwargs)  # type: ignore
        self.init()
