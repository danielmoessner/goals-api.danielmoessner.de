from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import ObjectDoesNotExist

from apps.todos.models import NeverEndingToDo, NormalToDo, RepetitiveToDo, PipelineToDo


class UserPassesToDoTestMixin(UserPassesTestMixin):
    def test_func(self):
        if self.get_object().user == self.request.user:
            return True
        return False


def get_todo_in_its_proper_class(pk):
    if NormalToDo.objects.filter(pk=pk).exists():
        return NormalToDo.objects.get(pk=pk)
    elif NeverEndingToDo.objects.filter(pk=pk).exists():
        return NeverEndingToDo.objects.get(pk=pk)
    elif RepetitiveToDo.objects.filter(pk=pk).exists():
        return RepetitiveToDo.objects.get(pk=pk)
    elif PipelineToDo.objects.filter(pk=pk).exists():
        return PipelineToDo.objects.get(pk=pk)
    raise ObjectDoesNotExist
