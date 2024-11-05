from rest_framework.decorators import action
from rest_framework.response import Response
from apps.todos.serializers import ToDoSerializer, NormalToDoSerializer, RepetitiveToDoSerializer, \
    NeverEndingToDoSerializer, PipelineToDoSerializer, RepetitiveToDoSerializerWithoutPrevious, \
    PipelineToDoSerializerWithoutPrevious, NeverEndingToDoSerializerWithoutPrevious
from apps.todos.models import ToDo, NormalToDo, RepetitiveToDo, NeverEndingToDo, PipelineToDo
from apps.todos.utils import get_todo_in_its_proper_class
from rest_framework import viewsets, permissions


class ToDoViewSet(viewsets.ModelViewSet):
    serializer_class = ToDoSerializer
    queryset = ToDo.objects.none()
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if type(instance) == NormalToDo:
            serializer = NormalToDoSerializer(instance, context={'request': request})
        elif type(instance) == RepetitiveToDo:
            serializer = RepetitiveToDoSerializer(instance, context={'request': request})
        elif type(instance) == NeverEndingToDo:
            serializer = NeverEndingToDoSerializer(instance, context={'request': request})
        elif type(instance) == PipelineToDo:
            serializer = PipelineToDoSerializer(instance, context={'request': request})
        else:
            raise Exception('No serializer was found.')
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def state(self, request):
        data = {
            "status": self.request.user.to_dos.count() + self.request.user.to_dos.filter(activate=None).count()
        }
        return Response(data)

    def get_object(self):
        obj = super().get_object()
        obj = get_todo_in_its_proper_class(obj.pk)
        return obj

    def get_queryset(self):
        return ToDo.get_to_dos_user(
            self.request.user,
            ToDo
        )

    def list(self, request, *args, **kwargs):
        normal_to_dos = ToDo.get_to_dos_user(
            self.request.user, NormalToDo
        )
        normal_to_dos_serializer = NormalToDoSerializer(normal_to_dos, many=True, context={'request': request})

        repetitive_to_dos = ToDo.get_to_dos_user(
            self.request.user, RepetitiveToDo
        )
        repetitive_to_dos_serializer = RepetitiveToDoSerializerWithoutPrevious(repetitive_to_dos, many=True,
                                                                               context={'request': request})
        never_ending_to_dos = ToDo.get_to_dos_user(
            self.request.user, NeverEndingToDo
        )
        never_ending_to_dos_serializer = NeverEndingToDoSerializerWithoutPrevious(never_ending_to_dos, many=True,
                                                                                  context={'request': request})
        pipeline_to_dos = ToDo.get_to_dos_user(
            self.request.user, PipelineToDo
        )
        pipeline_to_dos_serializer = PipelineToDoSerializerWithoutPrevious(pipeline_to_dos, many=True,
                                                                           context={'request': request})
        data = (
                normal_to_dos_serializer.data +
                repetitive_to_dos_serializer.data +
                never_ending_to_dos_serializer.data +
                pipeline_to_dos_serializer.data
        )
        return Response(data)


class NormalToDoViewSet(viewsets.ModelViewSet):
    serializer_class = NormalToDoSerializer
    queryset = NormalToDo.objects.none()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ToDo.get_to_dos_user(
            self.request.user, NormalToDo
        )

    def list(self, request, *args, **kwargs):
        queryset = ToDo.get_to_dos_user(
            self.request.user, NormalToDo
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RepetitiveToDoViewSet(viewsets.ModelViewSet):
    serializer_class = RepetitiveToDoSerializer
    queryset = RepetitiveToDo.objects.none()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ToDo.get_to_dos_user(
            self.request.user, RepetitiveToDo
        )

    def list(self, request, *args, **kwargs):
        queryset = ToDo.get_to_dos_user(
            self.request.user, RepetitiveToDo
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class NeverEndingToDoViewSet(viewsets.ModelViewSet):
    serializer_class = NeverEndingToDoSerializer
    queryset = NeverEndingToDo.objects.none()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ToDo.get_to_dos_user(
            self.request.user, NeverEndingToDo
        )

    def list(self, request, *args, **kwargs):
        queryset = ToDo.get_to_dos_user(
            self.request.user, NeverEndingToDo
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PipelineToDoViewSet(viewsets.ModelViewSet):
    serializer_class = PipelineToDoSerializer
    queryset = PipelineToDo.objects.none()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ToDo.get_to_dos_user(
            self.request.user, PipelineToDo
        )

    def list(self, request, *args, **kwargs):
        queryset = ToDo.get_to_dos_user(
            self.request.user, PipelineToDo
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
