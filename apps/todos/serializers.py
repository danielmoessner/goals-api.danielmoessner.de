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
    id = serializers.ReadOnlyField()

    class Meta:
        model = ToDo
        exclude = ['user']

    def save(self, **kwargs):
        if self.instance is not None:
            self.instance = get_todo_in_its_proper_class(self.instance.pk)
        return super().save(**kwargs)


class NormalToDoSerializer(AddUserMixin, serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='todos:normaltodo-detail')
    form_url = serializers.ReadOnlyField()
    id = serializers.ReadOnlyField()
    type = serializers.ReadOnlyField(default='NORMAL')

    class Meta:
        model = NormalToDo
        exclude = ['user']


class NeverEndingToDoSerializer(AddUserMixin, serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='todos:neverendingtodo-detail')
    previous = serializers.HyperlinkedRelatedField(view_name='todos:neverendingtodo-detail',
                                                   read_only=True)
    form_url = serializers.ReadOnlyField()
    id = serializers.ReadOnlyField()
    next = serializers.HyperlinkedRelatedField(view_name='todos:neverendingtodo-detail', read_only=True)
    type = serializers.ReadOnlyField(default='NEVER_ENDING')

    class Meta:
        model = NeverEndingToDo
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class RepetitiveToDoSerializer(AddUserMixin, serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='todos:repetitivetodo-detail')
    previous = serializers.HyperlinkedRelatedField(view_name='todos:repetitivetodo-detail',
                                                   queryset=RepetitiveToDo.objects.none(),
                                                   required=False)
    form_url = serializers.ReadOnlyField()
    id = serializers.ReadOnlyField()
    type = serializers.ReadOnlyField(default='REPETITIVE')

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
    form_url = serializers.ReadOnlyField()
    id = serializers.ReadOnlyField()
    type = serializers.ReadOnlyField(default='PIPELINE')

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
