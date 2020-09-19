from rest_framework.routers import DefaultRouter
from django.urls import path, include
from apps.todos import views
from apps.todos import api

router = DefaultRouter()
router.register(r'todos', api.ToDoViewSet)
router.register(r'normal-todos', api.NormalToDoViewSet)
router.register(r'repetitive-todos', api.RepetitiveToDoViewSet)
router.register(r'never-ending-todos', api.NeverEndingToDoViewSet)
router.register(r'pipeline-todos', api.PipelineToDoViewSet)

app_name = "todos"

urlpatterns = [
    # path('', views.ToDosView.as_view(), name="index"),
    path('api/', include(router.urls)),
    # path('all/', views.AllToDosView.as_view(), name="all"),
    # path('add', views.AddToDosView.as_view(), name='add'),
    # path('todo/<pk>/', views.ToDoView.as_view(), name="to_do"),
]
