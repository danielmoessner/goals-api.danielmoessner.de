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
    # views
    path('search', views.SearchView.as_view(), name='search'),
    path('starview', views.StarView.as_view(), name="star_view"),
    path('treeview', views.TreeView.as_view(), name="tree_view"),
    path('addview', views.AddView.as_view(), name="add_view"),
    path('alllinksview', views.AllLinksView.as_view(), name="all_links_view"),
    path('allprogressmonitorsview', views.AllProgressMonitorsView.as_view(), name="all_progress_monitors_view"),
    path('link/<pk>', views.LinkView.as_view(), name="link"),
    path('progressmonitor/<pk>', views.ProgressMonitorView.as_view(), name="progress_monitor"),
]


app_name = "goals"
