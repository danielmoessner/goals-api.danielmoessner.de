from django.utils import timezone
from rest_framework import serializers

from apps.todos.models import (
    NeverEndingTodo,
    NormalTodo,
    PipelineTodo,
    RepetitiveTodo,
    Todo,
)
from apps.todos.utils import get_todo_in_its_proper_class


class AddUserMixin:
    def validate(self, attrs):
        attrs = super().validate(attrs)
        if "user" not in attrs:
            attrs["user"] = self.context["request"].user
        return attrs


class ToDoSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="todo-detail")
    id = serializers.ReadOnlyField()

    class Meta:
        model = Todo
        exclude = ["user"]

    def save(self, **kwargs):
        if self.instance is not None:
            self.instance = get_todo_in_its_proper_class(self.instance.pk)
        return super().save(**kwargs)


class NormalToDoSerializer(AddUserMixin, serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="normaltodo-detail")
    id = serializers.ReadOnlyField()
    type = serializers.SerializerMethodField("get_type")

    def get_type(self, todo):
        return "NORMAL"

    class Meta:
        model = NormalTodo
        exclude = ["user"]


class NeverEndingToDoSerializer(AddUserMixin, serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="neverendingtodo-detail")
    previous = serializers.HyperlinkedRelatedField(
        view_name="neverendingtodo-detail", read_only=True
    )
    id = serializers.ReadOnlyField()
    next = serializers.HyperlinkedRelatedField(
        view_name="neverendingtodo-detail", read_only=True
    )
    type = serializers.SerializerMethodField("get_type")
    activate = serializers.DateTimeField(default=timezone.now)
    deadline = serializers.DateTimeField(required=False, read_only=True)

    def get_type(self, todo):
        return "NEVER_ENDING"

    class Meta:
        model = NeverEndingTodo
        exclude = ["user"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class NeverEndingToDoSerializerWithoutPrevious(NeverEndingToDoSerializer):
    previous = None
    next = None

    class Meta:
        model = NeverEndingTodo
        exclude = ["user", "previous"]


class RepetitiveToDoSerializer(AddUserMixin, serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="repetitivetodo-detail")
    previous = serializers.HyperlinkedRelatedField(
        view_name="repetitivetodo-detail", read_only=True, required=False
    )
    id = serializers.ReadOnlyField()
    type = serializers.SerializerMethodField("get_type")
    next = serializers.HyperlinkedRelatedField(
        view_name="repetitivetodo-detail", read_only=True
    )
    activate = serializers.DateTimeField(required=True)
    deadline = serializers.DateTimeField(required=True)
    repetitions = serializers.IntegerField(min_value=0, required=True)

    def get_type(self, todo):
        return "REPETITIVE"

    class Meta:
        model = RepetitiveTodo
        exclude = ["user"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class RepetitiveToDoSerializerWithoutPrevious(RepetitiveToDoSerializer):
    previous = None
    next = None

    class Meta:
        exclude = ["previous"]
        model = RepetitiveTodo


class PipelineToDoSerializerWithoutPrevious(
    AddUserMixin, serializers.HyperlinkedModelSerializer
):
    url = serializers.HyperlinkedIdentityField(view_name="pipelinetodo-detail")
    id = serializers.ReadOnlyField()
    type = serializers.SerializerMethodField("get_type")
    activate = serializers.ReadOnlyField()

    class Meta:
        model = PipelineTodo
        exclude = ["previous", "user"]

    def get_type(self, todo):
        return "PIPELINE"


class PipelineToDoSerializer(PipelineToDoSerializerWithoutPrevious):
    previous = serializers.HyperlinkedRelatedField(
        view_name="todo-detail", queryset=Todo.objects.none()
    )

    class Meta:
        model = PipelineTodo
        exclude = ["user"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["previous"].queryset = Todo.get_to_dos_user(
            self.context["request"].user, Todo
        )
