from django.contrib.auth.models import AbstractUser
from django.db.models import signals
from django.db import models

from datetime import timedelta


class CustomUser(AbstractUser):
    # init page
    PAGE_CHOICES = (
        ("DASHBOARD", "Dashboard View"),
        ("TO_DOS", "To Do's View"),
        ("TREE", "Tree View"),
        ("STAR", "Star View"),
        ("NOTES", "Notes View"),
    )
    page_choice = models.CharField(max_length=10, choices=PAGE_CHOICES, default="DASHBOARD")
    # star view
    GOAL_CHOICES = (
        ("ALL", "Show all goals."),
        ("STAR", "Show all starred goals."),
        ("UNREACHED", "Show all not yet achieved goals."),
        ("ACHIEVED", "Show all achieved goals."),
        ("DEPTH", "Show all goals within the depth range."),
        ("NONE", "Show no goals.")
    )
    goal_depth = models.PositiveSmallIntegerField(blank=True, null=True)
    goal_choice = models.CharField(max_length=10, choices=GOAL_CHOICES, default="ALL")
    PROGRESS_MONITOR_CHOICES = (
        ("ALL", "Show all progress monitors."),
        ("UNREACHED", "Show all not yet fully loaded progress monitors."),
        ("LOADED", "Show all fully loaded progress monitors."),
        ("RELATED", "Show goal related progress monitors."),
        ("NONE", "Show no progress monitors.")
    )
    progress_monitor_choice = models.CharField(max_length=10, choices=PROGRESS_MONITOR_CHOICES, default="ALL")
    LINK_CHOICES = (
        ("ALL", "Show all links."),
        ("RELATED", "Show master or sub goal related links."),
        ("XRELATED", "Show master and sub goal related links."),
        ("NONE", "Show no links.")
    )
    link_choice = models.CharField(max_length=10, choices=LINK_CHOICES, default="ALL")
    STRATEGY_CHOICES = (
        ("ALL", "Show all strategies."),
        ("STAR", "Show all starred strategies."),
        ("RELATED", "Show goal related strategies."),
        ("NONE", "Show no strategies.")
    )
    strategy_choice = models.CharField(max_length=10, choices=STRATEGY_CHOICES, default="ALL")
    # to dos view
    TO_DO_CHOICES = (
        ("ALL", "Show all to do's."),
        ("ACTIVE", "Show all active to do's"),
        ("UNFINISHED", "Show all unfinished to do's"),
        ("DELTA", "Show all to dos that are active and with a deadline within the delta range."),
        ("OVERDUE", "Show all to dos that are overdue."),
        ("ORANGE", "Show all to dos that are active or orange or red."),
        ("RELATED", "Show goal related to dos."),
        ("NONE", "Show no to do's.")
    )
    to_dos_delta = models.DurationField(blank=True, default=timedelta(days=7))
    normal_to_dos_choice = models.CharField(max_length=10, choices=TO_DO_CHOICES, default="ALL")
    repetitive_to_dos_choice = models.CharField(max_length=10, choices=TO_DO_CHOICES, default="ALL")
    never_ending_to_dos_choice = models.CharField(max_length=10, choices=TO_DO_CHOICES, default="ALL")
    multiple_to_dos_choice = models.CharField(max_length=10, choices=TO_DO_CHOICES, default="ALL")
    pipeline_to_dos_choice = models.CharField(max_length=10, choices=TO_DO_CHOICES, default="ALL")
