from typing import Generic, TypeVar

from django.db import models

T = TypeVar("T", bound=models.Model)


class GetInstance(Generic[T]):
    instance: T

    def get_instance_from_init_kwargs(self, **kwargs) -> T:
        return kwargs["instance"]
