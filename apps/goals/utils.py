from django.contrib.auth.mixins import UserPassesTestMixin


class UserPassesGoalTestMixin(UserPassesTestMixin):
    def test_func(self):
        if self.get_object().user == self.request.user:
            return True
        return False


class UserPassesStrategyTestMixin(UserPassesTestMixin):
    def test_func(self):
        if self.get_object().goal.user == self.request.user:
            return True
        return False


class UserPassesLinkTestMixin(UserPassesTestMixin):
    def test_func(self):
        if self.get_object().master_goal.user == self.request.user:
            return True
        return False


class UserPassesToDoTestMixin(UserPassesTestMixin):
    def test_func(self):
        if self.get_object().strategy.goal.user == self.request.user:
            return True
        return False


class UserPassesProgressMonitorTestMixin(UserPassesTestMixin):
    def test_func(self):
        if self.get_object().goal.user == self.request.user:
            return True
        return False
