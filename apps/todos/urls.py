from rest_framework.routers import DefaultRouter
from apps.todos import viewsets
from django.urls import path
from ..todos import views
from django.shortcuts import render


router = DefaultRouter()
router.register(r'todos', viewsets.ToDoViewSet)
router.register(r'normal-todos', viewsets.NormalToDoViewSet)
router.register(r'repetitive-todos', viewsets.RepetitiveToDoViewSet)
router.register(r'never-ending-todos', viewsets.NeverEndingToDoViewSet)
router.register(r'pipeline-todos', viewsets.PipelineToDoViewSet)

urlpatterns = [
    path("todos/", views.todos, name="todos"),
    path("wuerfel/", lambda r: render(r, "wuerfel.html")),
    path("<str:form_name>/", views.form_view, name="form"),
]
