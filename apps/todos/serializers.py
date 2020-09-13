from rest_framework import serializers
from apps.todos.models import ToDo, NeverEndingToDo, RepetitiveToDo, PipelineToDo, NormalToDo
from apps.todos.utils import get_todo_in_its_proper_class


class ToDoSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='todos:todo-detail')
    detail_url = serializers.ReadOnlyField()

    class Meta:
        model = ToDo
        # fields = ['id', 'name', 'activate', 'deadline', 'notes', 'is_archived', 'completed', 'status', 'url',
        #           'detail_url']
        exclude = ['user']
        # fields = '__all__'

    def save(self, **kwargs):
        if self.instance is not None:
            self.instance = get_todo_in_its_proper_class(self.instance.pk)
        return super().save(**kwargs)


class NormalToDoSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='todos:todo-detail')
    detail_url = serializers.ReadOnlyField()

    class Meta:
        model = NormalToDo
        exclude = ['user']


class NeverEndingToDoSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='todos:todo-detail')
    previous = serializers.HyperlinkedIdentityField(view_name='todos:todo-detail')
    detail_url = serializers.ReadOnlyField()

    class Meta:
        model = NeverEndingToDo
        exclude = ['user']


class RepetitiveToDoSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='todos:todo-detail')
    detail_url = serializers.ReadOnlyField()

    class Meta:
        model = RepetitiveToDo
        exclude = ['user']


class PipelineToDoSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='todos:todo-detail')
    detail_url = serializers.ReadOnlyField()

    class Meta:
        model = PipelineToDo
        exclude = ['user']
