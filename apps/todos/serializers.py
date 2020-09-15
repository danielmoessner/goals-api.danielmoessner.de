from django.utils import timezone

from apps.todos.models import ToDo, NeverEndingToDo, RepetitiveToDo, PipelineToDo, NormalToDo
from apps.todos.utils import get_todo_in_its_proper_class
from rest_framework import serializers


class AddUserMixin:
    def validate(self, attrs):
        attrs = super().validate(attrs)
        if 'user' not in attrs:
            attrs['user'] = self.context['request'].user
        return attrs


class ToDoSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='todos:todo-detail')
    detail_url = serializers.ReadOnlyField()

    class Meta:
        model = ToDo
        exclude = ['user']

    def save(self, **kwargs):
        if self.instance is not None:
            self.instance = get_todo_in_its_proper_class(self.instance.pk)
        return super().save(**kwargs)


class NormalToDoSerializer(AddUserMixin, serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='todos:normaltodo-detail')
    detail_url = serializers.ReadOnlyField()
    form_url = serializers.ReadOnlyField()

    class Meta:
        model = NormalToDo
        exclude = ['user']


class NeverEndingToDoSerializer(AddUserMixin, serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='todos:neverendingtodo-detail')
    previous = serializers.HyperlinkedRelatedField(view_name='todos:neverendingtodo-detail',
                                                   queryset=NeverEndingToDo.objects.none())
    detail_url = serializers.ReadOnlyField()
    form_url = serializers.ReadOnlyField()

    class Meta:
        model = NeverEndingToDo
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['previous'].queryset = ToDo.get_to_dos_user(
            self.context['request'].user,
            NeverEndingToDo,
            'ALL',
            include_archived_to_dos=False
        )


class RepetitiveToDoSerializer(AddUserMixin, serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='todos:repetitivetodo-detail')
    previous = serializers.HyperlinkedRelatedField(view_name='todos:repetitivetodo-detail',
                                                   queryset=RepetitiveToDo.objects.none(),
                                                   required=False)
    detail_url = serializers.ReadOnlyField()
    form_url = serializers.ReadOnlyField()

    class Meta:
        model = RepetitiveToDo
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['previous'].queryset = ToDo.get_to_dos_user(
            self.context['request'].user,
            RepetitiveToDo,
            'ALL',
            include_archived_to_dos=False
        )


class PipelineToDoSerializer(AddUserMixin, serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='todos:pipelinetodo-detail')
    previous = serializers.HyperlinkedRelatedField(view_name='todos:todo-detail', queryset=ToDo.objects.none())
    detail_url = serializers.ReadOnlyField()
    form_url = serializers.ReadOnlyField()

    class Meta:
        model = PipelineToDo
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['previous'].queryset = ToDo.get_to_dos_user(
            self.context['request'].user,
            ToDo,
            'ALL',
            include_archived_to_dos=False
        )
