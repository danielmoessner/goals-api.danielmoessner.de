from typing import TYPE_CHECKING

from django.contrib.auth.tokens import PasswordResetTokenGenerator

if TYPE_CHECKING:
    from apps.users.models import CustomUser


class ConfirmEmailTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user: "CustomUser", timestamp: int) -> str:
        return f"{user.pk}{user.email_confirmed}{user.email}"


class ChangeEmailTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user: "CustomUser", timestamp: int) -> str:
        return f"{user.pk}{user.email}{user.new_email}"
