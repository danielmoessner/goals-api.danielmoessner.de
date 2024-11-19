from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.todos.models import (
    NeverEndingTodo,
    NormalTodo,
    PipelineTodo,
    RepetitiveTodo,
    Todo,
)
from apps.todos.serializers import (
    NeverEndingToDoSerializer,
    NeverEndingToDoSerializerWithoutPrevious,
    NormalToDoSerializer,
    PipelineToDoSerializer,
    PipelineToDoSerializerWithoutPrevious,
    RepetitiveToDoSerializer,
    RepetitiveToDoSerializerWithoutPrevious,
    ToDoSerializer,
)
from apps.todos.utils import get_todo_in_its_proper_class


class ToDoViewSet(viewsets.ModelViewSet):
    serializer_class = ToDoSerializer
    queryset = Todo.objects.none()
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if type(instance) is NormalTodo:
            serializer = NormalToDoSerializer(instance, context={"request": request})
        elif type(instance) is RepetitiveTodo:
            serializer = RepetitiveToDoSerializer(
                instance, context={"request": request}
            )
        elif type(instance) is NeverEndingTodo:
            serializer = NeverEndingToDoSerializer(
                instance, context={"request": request}
            )
        elif type(instance) is PipelineTodo:
            serializer = PipelineToDoSerializer(instance, context={"request": request})
        else:
            raise Exception("No serializer was found.")
        return Response(serializer.data)

    @action(methods=["get"], detail=False)
    def state(self, request):
        data = {
            "status": self.request.user.to_dos.count()
            + self.request.user.to_dos.filter(activate=None).count()
        }
        return Response(data)

    def get_object(self):
        obj = super().get_object()
        obj = get_todo_in_its_proper_class(obj.pk)
        return obj

    def get_queryset(self):
        return Todo.get_to_dos_user(self.request.user, Todo)

    def list(self, request, *args, **kwargs):
        normal_to_dos = Todo.get_to_dos_user(self.request.user, NormalTodo)
        normal_to_dos_serializer = NormalToDoSerializer(
            normal_to_dos, many=True, context={"request": request}
        )

        repetitive_to_dos = Todo.get_to_dos_user(self.request.user, RepetitiveTodo)
        repetitive_to_dos_serializer = RepetitiveToDoSerializerWithoutPrevious(
            repetitive_to_dos, many=True, context={"request": request}
        )
        never_ending_to_dos = Todo.get_to_dos_user(self.request.user, NeverEndingTodo)
        never_ending_to_dos_serializer = NeverEndingToDoSerializerWithoutPrevious(
            never_ending_to_dos, many=True, context={"request": request}
        )
        pipeline_to_dos = Todo.get_to_dos_user(self.request.user, PipelineTodo)
        pipeline_to_dos_serializer = PipelineToDoSerializerWithoutPrevious(
            pipeline_to_dos, many=True, context={"request": request}
        )
        data = (
            normal_to_dos_serializer.data
            + repetitive_to_dos_serializer.data
            + never_ending_to_dos_serializer.data
            + pipeline_to_dos_serializer.data
        )
        return Response(data)


class NormalToDoViewSet(viewsets.ModelViewSet):
    serializer_class = NormalToDoSerializer
    queryset = NormalTodo.objects.none()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Todo.get_to_dos_user(self.request.user, NormalTodo)

    def list(self, request, *args, **kwargs):
        queryset = Todo.get_to_dos_user(self.request.user, NormalTodo)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RepetitiveToDoViewSet(viewsets.ModelViewSet):
    serializer_class = RepetitiveToDoSerializer
    queryset = RepetitiveTodo.objects.none()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Todo.get_to_dos_user(self.request.user, RepetitiveTodo)

    def list(self, request, *args, **kwargs):
        queryset = Todo.get_to_dos_user(self.request.user, RepetitiveTodo)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class NeverEndingToDoViewSet(viewsets.ModelViewSet):
    serializer_class = NeverEndingToDoSerializer
    queryset = NeverEndingTodo.objects.none()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Todo.get_to_dos_user(self.request.user, NeverEndingTodo)

    def list(self, request, *args, **kwargs):
        queryset = Todo.get_to_dos_user(self.request.user, NeverEndingTodo)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PipelineToDoViewSet(viewsets.ModelViewSet):
    serializer_class = PipelineToDoSerializer
    queryset = PipelineTodo.objects.none()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Todo.get_to_dos_user(self.request.user, PipelineTodo)

    def list(self, request, *args, **kwargs):
        queryset = Todo.get_to_dos_user(self.request.user, PipelineTodo)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
