from django.contrib.auth.mixins import UserPassesTestMixin


class UserPassesNoteTestMixin(UserPassesTestMixin):
    def test_func(self):
        if self.get_object().user == self.request.user:
            return True
        return False
