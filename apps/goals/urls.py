from django.urls import path

from apps.goals.views import views
from apps.goals.views import form_views
urlpatterns = [
    ###
    # Goal
    ###
    path('goal/list/', views.ListGoal.as_view(), name="all_goals_view"),
    path('goal/main/', views.MainGoal.as_view(), name="index"),
    path('goal/add/', form_views.CreateGoal.as_view(), name='goal_add'),
    path('goal/<pk>/', views.DetailGoal.as_view(), name="goal"),
    path('goal/<pk>/edit/', form_views.UpdateGoal.as_view(), name='goal_edit'),
    path('goal/<pk>/delete/', form_views.DeleteGoal.as_view(), name='goal_delete'),
    path('goal/<pk>/star/', form_views.UpdateStarGoal.as_view(), name='goal_star'),
    path('goal/<pk>/archive/', form_views.UpdateArchiveGoal.as_view(), name='goal_archive'),
    # progressmonitor
    path('progressmonitor/add', form_views.ProgressMonitorAdd.as_view(), name='progress_monitor_add'),
    path('progressmonitor/<pk>/edit', form_views.ProgressMonitorEdit.as_view(), name='progress_monitor_edit'),
    path('progressmonitor/<pk>/delete', form_views.ProgressMonitorDelete.as_view(), name='progress_monitor_delete'),
    path('progressmonitor/<pk>/step', form_views.ProgressMonitorStep.as_view(), name='progress_monitor_step'),
    # link
    path('link/add', form_views.LinkAdd.as_view(), name='link_add'),
    path('link/<pk>/edit', form_views.LinkEdit.as_view(), name='link_edit'),
    path('link/<pk>/delete', form_views.LinkDelete.as_view(), name='link_delete'),
    ###
    # Strategy
    ###
    path('strategy/list/', views.ListStrategy.as_view(), name="all_strategies_view"),
    path('strategy/main/', views.MainStrategy.as_view(), name='strategy_main'),
    path('strategy/add/', views.CreateStrategy.as_view(), name='strategy_add'),
    path('strategy/<pk>/edit/', views.UpdateStrategy.as_view(), name='strategy_edit'),
    path('strategy/<pk>/delete/', views.DeleteStrategy.as_view(), name='strategy_delete'),
    path('strategy/<pk>/star/', views.UpdateStarStrategy.as_view(), name='strategy_star'),
    path('strategy/<pk>/archive/', views.UpdateArchiveStrategy.as_view(), name='strategy_archive'),
    path('strategy/<pk>/', views.DetailStrategy.as_view(), name="strategy"),
    # todos
    path('todo/add', form_views.ToDoAdd.as_view(), name='to_do_add'),
    path('todo/<pk>/edit', form_views.ToDoEdit.as_view(), name='to_do_edit'),
    path('todo/<pk>/delete', form_views.ToDoDelete.as_view(), name='to_do_delete'),
    path('todo/<pk>/done', form_views.ToDoDone.as_view(), name='to_do_done'),
    path('todo/<pk>/failed', form_views.ToDoFailed.as_view(), name='to_do_failed'),
    path('todo/<pk>/notes', form_views.ToDoNotes.as_view(), name='to_do_notes'),
    path('repetitivetodo/add', form_views.RepetitiveToDoAdd.as_view(), name='repetitive_to_do_add'),
    path('repetitivetodo/<pk>/edit', form_views.RepetitiveToDoEdit.as_view(), name='repetitive_to_do_edit'),
    path('repetitivetodo/<pk>/delete', form_views.RepetitiveToDoDelete.as_view(), name='repetitive_to_do_delete'),
    path('repetitivetodo/<pk>/delete-list', form_views.RepetitiveToDoListDelete.as_view(),
         name='repetitive_to_do_list_delete'),
    path('repetitivetodo/<pk>/done', form_views.RepetitiveToDoDone.as_view(), name='repetitive_to_do_done'),
    path('repetitivetodo/<pk>/failed', form_views.RepetitiveToDoFailed.as_view(), name='repetitive_to_do_failed'),
    path('neverendingtodo/add', form_views.NeverEndingToDoAdd.as_view(), name='never_ending_to_do_add'),
    path('neverendingtodo/<pk>/edit', form_views.NeverEndingToDoEdit.as_view(), name='never_ending_to_do_edit'),
    path('neverendingtodo/<pk>/delete', form_views.NeverEndingToDoDelete.as_view(), name='never_ending_to_do_delete'),
    path('neverendingtodo/<pk>/done', form_views.NeverEndingToDoDone.as_view(), name='never_ending_to_do_done'),
    path('neverendingtodo/<pk>/failed', form_views.NeverEndingToDoFailed.as_view(), name='never_ending_to_do_failed'),
    path('pipelinetodo/add', form_views.PipelineToDoAdd.as_view(), name='pipeline_to_do_add'),
    path('pipelinetodo/<pk>/edit', form_views.PipelineToDoEdit.as_view(), name='pipeline_to_do_edit'),
    path('pipelinetodo/<pk>/delete', form_views.PipelineToDoDelete.as_view(), name='pipeline_to_do_delete'),
    path('pipelinetodo/<pk>/done', form_views.PipelineToDoDone.as_view(), name='pipeline_to_do_done'),
    path('pipelinetodo/<pk>/failed', form_views.PipelineToDoFailed.as_view(), name='pipeline_to_do_failed'),
    # views
    path('search', views.SearchView.as_view(), name='search'),
    path('test', views.TestView.as_view(), name="test"),
    path('starview', views.StarView.as_view(), name="star_view"),
    path('treeview', views.TreeView.as_view(), name="tree_view"),
    path('todosview', views.ToDosView.as_view(), name="to_dos_view"),
    path('addview', views.AddView.as_view(), name="add_view"),
    path('alllinksview', views.AllLinksView.as_view(), name="all_links_view"),
    path('allprogressmonitorsview', views.AllProgressMonitorsView.as_view(), name="all_progress_monitors_view"),
    path('alltodosview', views.AllToDosView.as_view(), name="all_to_dos_view"),
    path('todo/<pk>', views.ToDoView.as_view(), name="to_do"),
    path('link/<pk>', views.LinkView.as_view(), name="link"),
    path('progressmonitor/<pk>', views.ProgressMonitorView.as_view(), name="progress_monitor"),
    path('neverendingtodo/<pk>', views.NeverEndingToDoView.as_view(), name="never_ending_to_do"),
    path('repetitivetodo/<pk>', views.RepetitiveToDoView.as_view(), name="repetitive_to_do"),
    path('pipelinetodo/<pk>', views.PipelineToDoView.as_view(), name="pipeline_to_do"),
]


app_name = "goals"
