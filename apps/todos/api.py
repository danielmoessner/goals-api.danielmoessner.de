from django.utils import timezone
from rest_framework import status, mixins, generics, viewsets, renderers
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from apps.todos.serializers import ToDoSerializer, NormalToDoSerializer, RepetitiveToDoSerializer, \
    NeverEndingToDoSerializer, PipelineToDoSerializer
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from apps.todos.models import ToDo, NormalToDo, RepetitiveToDo, NeverEndingToDo, PipelineToDo


class ToDoViewSet(viewsets.ModelViewSet):
    """
    """
    serializer_class = ToDoSerializer
    queryset = ToDo.objects.none()

    def get_queryset(self):
        return ToDo.get_to_dos_user(
            self.request.user,
            ToDo,
            'ALL',
            delta=self.request.user.to_dos_delta,
            include_archived_to_dos=self.request.user.show_archived_objects
        )

    @action(detail=False, methods=['get'])
    def main(self, request):
        user = request.user
        normal_to_dos = ToDo.get_to_dos_user(
            user,
            NormalToDo,
            user.normal_to_dos_choice,
            delta=user.to_dos_delta,
            include_archived_to_dos=self.request.user.show_archived_objects
        )
        normal_to_dos_serializer = NormalToDoSerializer(normal_to_dos, many=True, context={'request': request})
        repetitive_to_dos = ToDo.get_to_dos_user(
            user,
            RepetitiveToDo,
            user.repetitive_to_dos_choice,
            delta=user.to_dos_delta,
            include_archived_to_dos=self.request.user.show_archived_objects
        )
        repetitive_to_dos_serializer = RepetitiveToDoSerializer(repetitive_to_dos, many=True,
                                                                context={'request': request})
        never_ending_to_dos = ToDo.get_to_dos_user(
            user,
            NeverEndingToDo,
            user.never_ending_to_dos_choice,
            delta=user.to_dos_delta,
            include_archived_to_dos=self.request.user.show_archived_objects
        )
        never_ending_to_dos_serializer = NeverEndingToDoSerializer(never_ending_to_dos, many=True,
                                                                   context={'request': request})
        pipeline_to_dos = ToDo.get_to_dos_user(
            user,
            PipelineToDo,
            user.pipeline_to_dos_choice,
            delta=user.to_dos_delta,
            include_archived_to_dos=self.request.user.show_archived_objects
        )
        pipeline_to_dos_serializer = PipelineToDoSerializer(pipeline_to_dos, many=True, context={'request': request})
        data = (
                normal_to_dos_serializer.data +
                repetitive_to_dos_serializer.data +
                never_ending_to_dos_serializer.data +
                pipeline_to_dos_serializer.data
        )
        return Response(data)

    @action(detail=False, methods=['get'])
    def done_today(self, request):
        queryset = ToDo.get_to_dos_user(
            request.user,
            ToDo,
            'ALL',
            include_archived_to_dos=True
        ).filter(
            completed__contains=timezone.now().date(),
            status='DONE'
        )
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def all(self, request):
        normal_to_dos = ToDo.get_to_dos_user(
            self.request.user, NormalToDo, 'ALL',
            include_archived_to_dos=self.request.user.show_archived_objects
        )
        normal_to_dos_serializer = NormalToDoSerializer(normal_to_dos, many=True, context={'request': request})
        repetitive_to_dos = ToDo.get_to_dos_user(
            self.request.user, RepetitiveToDo, 'ALL',
            include_archived_to_dos=self.request.user.show_archived_objects
        )
        repetitive_to_dos_serializer = RepetitiveToDoSerializer(normal_to_dos_serializer, many=True,
                                                                context={'request': request})
        never_ending_to_dos = ToDo.get_to_dos_user(
            self.request.user, NeverEndingToDo, 'ALL',
            include_archived_to_dos=self.request.user.show_archived_objects
        )
        never_ending_to_dos_serializer = NeverEndingToDoSerializer(never_ending_to_dos, many=True,
                                                                   context={'request': request})
        pipeline_to_dos = ToDo.get_to_dos_user(
            self.request.user, PipelineToDo, 'ALL',
            include_archived_to_dos=self.request.user.show_archived_objects
        )
        pipeline_to_dos_serializer = PipelineToDoSerializer(pipeline_to_dos, many=True, context={'request': request})
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

    def get_queryset(self):
        return ToDo.get_to_dos_user(
            self.request.user, NormalToDo, 'ALL',
            include_archived_to_dos=self.request.user.show_archived_objects
        )


class RepetitiveToDoViewSet(viewsets.ModelViewSet):
    serializer_class = RepetitiveToDoSerializer
    queryset = RepetitiveToDo.objects.none()

    def get_queryset(self):
        return ToDo.get_to_dos_user(
            self.request.user, RepetitiveToDo, 'ALL',
            include_archived_to_dos=self.request.user.show_archived_objects
        )


class NeverEndingToDoViewSet(viewsets.ModelViewSet):
    serializer_class = NeverEndingToDoSerializer
    queryset = NeverEndingToDo.objects.none()

    def get_queryset(self):
        return ToDo.get_to_dos_user(
            self.request.user, NeverEndingToDo, 'ALL',
            include_archived_to_dos=self.request.user.show_archived_objects
        )


class PipelineToDoViewSet(viewsets.ModelViewSet):
    serializer_class = PipelineToDoSerializer
    queryset = PipelineToDo.objects.none()

    def get_queryset(self):
        return ToDo.get_to_dos_user(
            self.request.user, PipelineToDo, 'ALL',
            include_archived_to_dos=self.request.user.show_archived_objects
        )

# @api_view(['GET'])
# def api_root(request, format=None):
#     return Response({
#         'to-dos': reverse('to-do-list', request=request, format=format),
#     })
#
#
# class ToDoList(generics.ListCreateAPIView):
#     queryset = ToDo.objects.all()
#     serializer_class = ToDoSerializer
#
#
# class ToDoDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = ToDo.objects.all()
#     serializer_class = ToDoSerializer

#
# class ToDoList(APIView):
#     """
#     List all snippets, or create a new snippet.
#     """
#
#     def get(self, request, format=None):
#         todos = ToDo.objects.all()
#         serializer = ToDoSerializer(todos, many=True, context={'request': request})
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = ToDoSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class ToDoDetail(mixins.RetrieveModelMixin,
#                  mixins.UpdateModelMixin,
#                  mixins.DestroyModelMixin,
#                  generics.GenericAPIView):
#     queryset = ToDo.objects.all()
#     serializer_class = ToDoSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
