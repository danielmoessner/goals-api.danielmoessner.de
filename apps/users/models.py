from django.contrib.auth.models import AbstractUser
from django.db import models

from datetime import timedelta


class CustomUser(AbstractUser):
    # choices
    PAGE_CHOICES = (
        ("DASHBOARD", "Dashboard View"),
        ("TO_DOS", "To Do's View"),
        ("TREE", "Tree View"),
        ("STAR", "Star View"),
        ("NOTES", "Notes View"),
    )
    GOAL_CHOICES = (
        ('ALL', "Show all goals."),
        ('ACTIVE', 'Show all goals that are considered active.'),
        ("STAR", "Show all starred goals."),
        ("UNREACHED", "Show all not yet achieved goals."),
        ("ACHIEVED", "Show all achieved goals."),
        ("DEPTH", "Show all goals within the depth range."),
        ('ARCHIVE', "Show all goals that are in the archive."),
        ("NONE", "Show no goals.")
    )
    PROGRESS_MONITOR_CHOICES = (
        ('ALL', "Show all progress monitors."),
        ("UNREACHED", "Show all not yet fully loaded progress monitors."),
        ("LOADED", "Show all fully loaded progress monitors."),
        ("NONE", "Show no progress monitors.")
    )
    LINK_CHOICES = (
        ('ALL', "Show all links."),
        ("NONE", "Show no links.")
    )
    STRATEGY_CHOICES = (
        ('ALL', "Show all strategies."),
        ("ACTIVE", "Show all strategies considered active."),
        ("STAR", "Show all starred strategies."),
        ("NONE", "Show no strategies.")
    )
    # make email the default login method
    username = None
    email = models.EmailField('E-Mail Address', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    # goals
    show_archived_objects = models.BooleanField(default=False)
    # goal view
    goal_view_goal_choice = models.CharField(max_length=10, choices=GOAL_CHOICES, default='ALL') # remove
    # strategy main
    strategy_main_choice = models.CharField(max_length=10, choices=STRATEGY_CHOICES, default='ALL') # remove
    # to do
    show_old_todos = models.BooleanField(default=False)
    # tree view
    treeview_goal_depth = models.PositiveSmallIntegerField(blank=True, null=True) # remove
    treeview_goal_choice = models.CharField(max_length=10, choices=GOAL_CHOICES, default='ALL')# remove
    treeview_monitor_choice = models.CharField(max_length=10, choices=PROGRESS_MONITOR_CHOICES, default='ALL')# remove
    treeview_strategy_choice = models.CharField(max_length=10, choices=STRATEGY_CHOICES, default='ALL')# remove

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
