from rest_framework.routers import DefaultRouter
from apps.todos import viewsets

router = DefaultRouter()
router.register(r'todos', viewsets.ToDoViewSet)
router.register(r'normal-todos', viewsets.NormalToDoViewSet)
router.register(r'repetitive-todos', viewsets.RepetitiveToDoViewSet)
router.register(r'never-ending-todos', viewsets.NeverEndingToDoViewSet)
router.register(r'pipeline-todos', viewsets.PipelineToDoViewSet)
