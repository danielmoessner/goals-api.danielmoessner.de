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
    TO_DO_CHOICES = (
        ('ALL', "Show all to do's."),
        ("ACTIVE", "Show all active to do's"),
        ("UNFINISHED", "Show all unfinished to do's"),
        ("DELTA", "Show all to dos that are active and with a deadline within the delta range."),
        ("OVERDUE", "Show all to dos that are overdue."),
        ("ORANGE", "Show all to dos that are active or orange or red."),
        ("NONE", "Show no to do's.")
    )
    # general
    page_choice = models.CharField(max_length=10, choices=PAGE_CHOICES, default="DASHBOARD")
    show_archived_objects = models.BooleanField(default=False)
    # goal view
    goal_view_goal_choice = models.CharField(max_length=10, choices=GOAL_CHOICES, default='ALL')
    # strategy main
    strategy_main_choice = models.CharField(max_length=10, choices=STRATEGY_CHOICES, default='ALL')
    # to do view
    to_dos_delta = models.DurationField(blank=True, default=timedelta(days=7))
    normal_to_dos_choice = models.CharField(max_length=10, choices=TO_DO_CHOICES, default='ALL')
    repetitive_to_dos_choice = models.CharField(max_length=10, choices=TO_DO_CHOICES, default='ALL')
    never_ending_to_dos_choice = models.CharField(max_length=10, choices=TO_DO_CHOICES, default='ALL')
    pipeline_to_dos_choice = models.CharField(max_length=10, choices=TO_DO_CHOICES, default='ALL')
    # tree view
    treeview_goal_depth = models.PositiveSmallIntegerField(blank=True, null=True)
    treeview_goal_choice = models.CharField(max_length=10, choices=GOAL_CHOICES, default='ALL')
    treeview_monitor_choice = models.CharField(max_length=10, choices=PROGRESS_MONITOR_CHOICES, default='ALL')
    treeview_strategy_choice = models.CharField(max_length=10, choices=STRATEGY_CHOICES, default='ALL')
    treeview_todos_delta = models.DurationField(blank=True, default=timedelta(days=7))
    treeview_normaltodos_choice = models.CharField(max_length=10, choices=TO_DO_CHOICES, default='ALL')
    treeview_repetitivetodos_choice = models.CharField(max_length=10, choices=TO_DO_CHOICES, default='ALL')
    treeview_neverendingtodos_choice = models.CharField(max_length=10, choices=TO_DO_CHOICES, default='ALL')
    treeview_pipelinetodos_choice = models.CharField(max_length=10, choices=TO_DO_CHOICES, default='ALL')
