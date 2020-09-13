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
    path('', views.ToDosView.as_view(), name="index"),
    path('all/', views.AllToDosView.as_view(), name="all"),
    path('api/', include(router.urls)),
    ###
    # ParentToDo
    ###
    path('todo/<pk>/done/', views.ToDoDone.as_view(), name='to_do_done'),
    path('todo/<pk>/notes/', views.ToDoNotes.as_view(), name='to_do_notes'),
    path('todo/<pk>/is-archived/', views.ToDoIsArchived.as_view(), name='to_do_is_archived'),
    path('todo/<pk>/status/', views.ToDoStatus.as_view(), name='to_do_status'),
    path('todo/<pk>/update/', views.ToDoUpdate.as_view(), name='to_do_update'),
    path('todo/<pk>/', views.ToDoView.as_view(), name="to_do"),
    ###
    # NormalToDo
    ###
    path('normaltodo/add/', views.NormalToDoAdd.as_view(), name='normal_to_do_add'),
    path('normaltodo/<pk>/edit/', views.NormalToDoEdit.as_view(), name='normal_to_do_edit'),
    path('normaltodo/<pk>/delete/', views.NormalToDoDelete.as_view(), name='normal_to_do_delete'),
    path('normaltodo/<pk>/done/', views.NormalToDoDone.as_view(), name='normal_to_do_done'),
    path('normaltodo/<pk>/failed/', views.NormalToDoFailed.as_view(), name='normal_to_do_failed'),
    path('normaltodo/<pk>/', views.NormalToDoView.as_view(), name='normal_to_do'),
    ###
    # RepetitiveToDo
    ###
    path('repetitivetodo/add/', views.RepetitiveToDoAdd.as_view(), name='repetitive_to_do_add'),
    path('repetitivetodo/<pk>/edit/', views.RepetitiveToDoEdit.as_view(), name='repetitive_to_do_edit'),
    path('repetitivetodo/<pk>/delete/', views.RepetitiveToDoDelete.as_view(), name='repetitive_to_do_delete'),
    path('repetitivetodo/<pk>/delete-list/', views.RepetitiveToDoListDelete.as_view(),
         name='repetitive_to_do_list_delete'),
    path('repetitivetodo/<pk>/done/', views.RepetitiveToDoDone.as_view(), name='repetitive_to_do_done'),
    path('repetitivetodo/<pk>/failed/', views.RepetitiveToDoFailed.as_view(), name='repetitive_to_do_failed'),
    path('repetitivetodo/<pk>/', views.RepetitiveToDoView.as_view(), name="repetitive_to_do"),
    ###
    # NeverEndingToDo
    ###
    path('neverendingtodo/add/', views.NeverEndingToDoAdd.as_view(), name='never_ending_to_do_add'),
    path('neverendingtodo/<pk>/edit/', views.NeverEndingToDoEdit.as_view(), name='never_ending_to_do_edit'),
    path('neverendingtodo/<pk>/delete/', views.NeverEndingToDoDelete.as_view(), name='never_ending_to_do_delete'),
    path('neverendingtodo/<pk>/done/', views.NeverEndingToDoDone.as_view(), name='never_ending_to_do_done'),
    path('neverendingtodo/<pk>/failed/', views.NeverEndingToDoFailed.as_view(), name='never_ending_to_do_failed'),
    path('neverendingtodo/<pk>/', views.NeverEndingToDoView.as_view(), name="never_ending_to_do"),
    ###
    # PipelineToDo
    ###
    path('pipelinetodo/add/', views.PipelineToDoAdd.as_view(), name='pipeline_to_do_add'),
    path('pipelinetodo/<pk>/edit/', views.PipelineToDoEdit.as_view(), name='pipeline_to_do_edit'),
    path('pipelinetodo/<pk>/delete/', views.PipelineToDoDelete.as_view(), name='pipeline_to_do_delete'),
    path('pipelinetodo/<pk>/done/', views.PipelineToDoDone.as_view(), name='pipeline_to_do_done'),
    path('pipelinetodo/<pk>/failed/', views.PipelineToDoFailed.as_view(), name='pipeline_to_do_failed'),
    path('pipelinetodo/<pk>/', views.PipelineToDoView.as_view(), name="pipeline_to_do"),
]
