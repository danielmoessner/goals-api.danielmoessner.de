from apps.users.models import CustomUser
from django.db.models import Q
from django.utils import timezone
from django.db import models


def g_all_filter():
    return Q()


def g_active_filter():
    return Q(progress__lt=100)


def g_star_filter():
    return Q(is_starred=True)


def g_unreached_filter():
    return Q(progress__lt=100)


def g_achieved_filter():
    return Q(progress__gte=100)


def g_archive_filter():
    return Q()


def g_depth_filter():
    return Q(False)


def g_none_filter():
    return Q(pk=None)


def m_all_filter():
    return Q()


def m_unreached_filter():
    return Q(progress_lt=100)


def m_loaded_filter():
    return Q(progress_gte=100)


def m_none_filter():
    return Q(pk=None)


def l_all_filter():
    return Q()


def l_none_filter():
    return Q(pk=None)


def s_all_filter():
    return Q()


def s_star_filter():
    return Q(is_starred=True)


def s_active_filter():
    return Q(progress__lt=100)


def s_none_filter():
    return Q(pk=None)


class Goal(models.Model):
    user = models.ForeignKey(CustomUser, related_name='goals', on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    why = models.TextField(blank=True, null=True)
    impact = models.TextField(blank=True, null=True)
    deadline = models.DateTimeField(null=True, blank=True)
    sub_goals = models.ManyToManyField(to='self', through='Link', symmetrical=False, related_name='master_goals')
    is_archived = models.BooleanField(default=False)
    addition = models.TextField(blank=True, null=True)
    # speed
    progress = models.PositiveSmallIntegerField(default=0, blank=True)
    # user
    is_starred = models.BooleanField(default=False)

    # general
    class Meta:
        ordering = ('is_archived', 'name')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for goal in list(self.master_goals.all()):
            goal.reset()

    def delete(self, *args, **kwargs):
        goals = list(self.master_goals.all())
        super().delete(*args, **kwargs)
        for goal in goals:
            goal.reset()

    # getters
    @staticmethod
    def get_goals(goals, goal_filter, include_archived_goals=False):
        if goal_filter == "ALL":
            goals = goals.filter(g_all_filter())
        elif goal_filter == 'ACTIVE':
            goals = goals.filter(g_active_filter())
        elif goal_filter == "STAR":
            goals = goals.filter(g_star_filter())
        elif goal_filter == "UNREACHED":
            goals = goals.exclude(g_unreached_filter())
        elif goal_filter == "ACHIEVED":
            goals = goals.filter(g_achieved_filter())
        elif goal_filter == "DEPTH" and False:
            goals = goals.filter(g_depth_filter())
        elif goal_filter == 'ARCHIVE':
            goals = goals.filter(g_archive_filter())
        else:
            goals = goals.filter(g_none_filter())
        if not include_archived_goals:
            goals = goals.filter(is_archived=False)
        return goals

    @staticmethod
    def get_goals_user(user, choice, include_archived_goals=False):
        goals = user.goals.all()
        goals = Goal.get_goals(goals, choice, include_archived_goals)
        return goals

    def get_tree_subgoals(self, user):
        queryset = self.sub_goals.all()
        queryset = Goal.get_goals(
            queryset,
            user.treeview_goal_choice,
            include_archived_goals=user.show_archived_objects
        )
        return queryset

    def get_tree_monitors(self, user):
        queryset = self.progress_monitors.all()
        queryset = ProgressMonitor.get_monitors(queryset, user.treeview_monitor_choice,
                                                included_archived_progress_monitors=user.show_archived_objects)
        return queryset

    def get_tree_strategies(self, user):
        queryset = self.strategies.all()
        queryset = Strategy.get_strategies(queryset, user.treeview_strategy_choice,
                                           include_archived_strategies=user.show_archived_objects)
        return queryset

    def get_all_sub_goals(self):
        query = self.sub_goals.all()
        for goal in self.sub_goals.all():
            query = query | goal.get_all_sub_goals()
        return query

    def get_all_sub_monitors(self):
        query = self.progress_monitors.all()
        for goal in self.get_all_sub_goals():
            query = query | goal.progress_monitors.all()
        return query

    def get_all_sub_strategies(self):
        query = self.strategies.all()
        for goal in self.get_all_sub_goals():
            query = query | goal.strategies.all()
        return query

    def get_all_sub_links(self):
        query = self.sub_links.all()
        for goal in self.get_all_sub_goals():
            query = query | goal.sub_links.all()
        return query

    def get_all_master_objects(self):
        objects = list()
        links = list(self.master_links.all())
        objects += links
        for link in links:
            objects += link.get_all_master_objects()
        return objects

    def get_all_mastergoals(self):
        query = self.master_goals.all()
        for goal in self.master_goals.all():
            query = query | goal.get_all_mastergoals()
        return query

    def get_progress_calc(self):
        progress = 0
        weight = 0

        for monitor in self.progress_monitors.all():
            progress += monitor.progress * monitor.weight
            weight += monitor.weight

        for link in self.sub_links.all():
            progress += link.progress * link.weight
            weight += link.weight

        return int(round(progress / weight))

    # setters
    def reset(self):
        self.progress = self.get_progress_calc()
        self.save()


class ProgressMonitor(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='progress_monitors')
    name = models.CharField(max_length=300)
    weight = models.PositiveSmallIntegerField(default=1)
    steps = models.PositiveSmallIntegerField()
    step = models.PositiveSmallIntegerField(default=0, blank=True)
    notes = models.TextField(default='', blank=True)
    is_archived = models.BooleanField(default=False)

    # general
    @property
    def progress(self):
        return round((float(self.step) / float(self.steps)) * 100) if self.steps != 0 else 100

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.step > self.steps:
            self.step = self.steps
        if self.step < 0:
            self.step = 0
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
        # calculate the goals progress
        self.goal.reset()

    class Meta:
        ordering = ('is_archived', 'name', 'goal')

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        goal = self.goal
        super(ProgressMonitor, self).delete(using=using, keep_parents=keep_parents)
        goal.reset()

    # getters
    @staticmethod
    def get_monitors(monitors, choice, included_archived_progress_monitors=False):
        if choice == "ALL":
            monitors = monitors.filter(m_all_filter())
        elif choice == "UNREACHED":
            monitors = monitors.filter(m_unreached_filter())
        elif choice == "LOADED":
            monitors = monitors.filter(m_loaded_filter())
        else:
            monitors = monitors.filter(m_none_filter())
        if not included_archived_progress_monitors:
            monitors = monitors.filter(is_archived=False)
        return monitors

    @staticmethod
    def get_monitors_user(user, monitor_filter, included_archived_progress_monitors=False):
        goals = Goal.get_goals_user(user, "ALL", include_archived_goals=included_archived_progress_monitors)
        monitors = ProgressMonitor.objects.filter(goal__in=goals)
        monitors = ProgressMonitor.get_monitors(monitors, monitor_filter, included_archived_progress_monitors)
        return monitors

    def get_all_master_objects(self):
        objects = list()
        objects += [self.goal]
        objects += self.goal.get_all_master_objects()
        return objects

    def get_notes(self):
        if self.notes:
            return self.notes
        return ''

    def get_tree(self):
        data = dict()
        data['name'] = self.name
        data['progress'] = self.progress
        data['pk'] = self.pk
        return data


class Link(models.Model):
    master_goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name="sub_links")
    sub_goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name="master_links")
    weight = models.PositiveSmallIntegerField(default=1)
    is_archived = models.BooleanField(default=False)

    # general
    @property
    def progress(self):
        return self.sub_goal.progress

    class Meta:
        ordering = ('is_archived', 'master_goal')

    def __str__(self):
        return self.get_name()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
        # reset the master goal progress
        self.master_goal.reset()

    def delete(self, using=None, keep_parents=False):
        master_goal = self.master_goal
        super(Link, self).delete(using=using, keep_parents=keep_parents)
        master_goal.reset()

    # getters
    @staticmethod
    def get_links(links, choice, include_archived_links=False):
        if choice == "ALL":
            links = links.filter(l_all_filter())
        else:
            links = links.filter(l_none_filter())
        if not include_archived_links:
            links.filter(is_archived=False)
        return links

    @staticmethod
    def get_links_user(user, link_filter, include_archived_links=False):
        goals = Goal.get_goals_user(user, "ALL")
        links = Link.objects.filter(master_goal__in=goals, sub_goal__in=goals)
        links = Link.get_links(links, link_filter, include_archived_links)
        return links

    def get_all_master_objects(self):
        objects = list()
        objects += [self.master_goal]
        objects += self.master_goal.get_all_master_objects()
        return objects

    def get_all_sub_goals(self):
        query = Goal.objects.filter(pk=self.sub_goal.pk)
        query = query | self.sub_goal.get_all_sub_goals()
        return query

    def get_all_sub_strategies(self):
        return self.sub_goal.get_all_sub_strategies()

    def get_all_sub_links(self):
        return self.sub_goal.get_all_sub_links()

    def get_all_sub_monitors(self):
        return self.sub_goal.get_all_sub_monitors()

    def get_name(self):
        return self.master_goal.name + ' --> ' + self.sub_goal.name


class Strategy(models.Model):
    name = models.CharField(max_length=300)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name="strategies")
    description = models.TextField(null=True, blank=True)
    is_archived = models.BooleanField(default=False)
    # user
    is_starred = models.BooleanField(default=False)

    # general
    class Meta:
        ordering = ('is_archived', 'name')

    def __str__(self):
        return str(self.name)

    # getters
    @staticmethod
    def get_strategies(strategies, strategy_filter, include_archived_strategies=False):
        if strategy_filter == "ALL":
            strategies = strategies.filter(s_all_filter())
        elif strategy_filter == "STAR":
            strategies = strategies.filter(s_star_filter())
        elif strategy_filter == 'ACTIVE':
            strategies = strategies.filter(s_active_filter())
        else:
            strategies = strategies.filter(s_none_filter())
        if not include_archived_strategies:
            strategies = strategies.filter(is_archived=False)
        return strategies

    @staticmethod
    def get_strategies_goals(goals, strategy_filter, include_archived_strategies=False):
        strategies = Strategy.objects.filter(goal__in=goals)

        strategies = Strategy.get_strategies(strategies, strategy_filter, include_archived_strategies)

        return strategies

    @staticmethod
    def get_strategies_user(user, strategy_filter, include_archived_strategies=False):
        goals = Goal.get_goals_user(user, "ALL", include_archived_goals=include_archived_strategies)
        strategies = Strategy.get_strategies_goals(goals, strategy_filter, include_archived_strategies)
        return strategies

    def get_all_master_objects(self):
        objects = list()
        objects += [self.goal]
        objects += self.goal.get_all_master_objects()
        return objects
