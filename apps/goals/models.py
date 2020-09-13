from django.db.models import Q, F
from django.utils import timezone
from django.db import models

from apps.users.models import CustomUser
from apps.core.utils import strfdelta

from datetime import timedelta


def td_all_filter():
    return Q()


def td_unfinished_filter():
    return Q(is_done=False, has_failed=False)


def td_active_filter():
    return Q(activate__lte=timezone.now(), is_done=False, has_failed=False)


def td_overdue_filter():
    return Q(deadline__lte=timezone.now(), is_done=False, has_failed=False)


def td_delta_filter(delta):
    return Q(deadline__lte=timezone.now() + delta, activate__lte=timezone.now(), is_done=False, has_failed=False)


def td_orange_filter():
    return Q(activate__lte=timezone.now(), is_done=False, has_failed=False)


def td_none_filter():
    return Q(pk=None)


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
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
        # reset the progress of all master links
        for link in self.master_links.all():
            link.reset()

    class Meta:
        ordering = ('is_archived', 'progress', 'deadline', 'name')

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        links = self.master_links.all()
        super(Goal, self).delete(using=using, keep_parents=keep_parents)
        for link in links:
            link.reset()

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

    def get_progress(self):
        if self.progress == 100:
            return 'achieved'
        return str(self.progress) + '%'

    def get_mastergoals(self):
        return ', '.join([goal.name for goal in self.master_goals.all()])

    def get_subgoals(self):
        return ', '.join([goal.name for goal in self.sub_goals.all()])

    def get_strategies(self):
        return ', '.join([strategy.name for strategy in self.strategies.all()])

    def get_deadline(self, accuracy='s'):
        if self.deadline:
            if accuracy is 'd':
                return timezone.localtime(self.deadline).strftime("%d.%m.%Y")
            if accuracy is 's':
                return timezone.localtime(self.deadline).strftime("%d.%m.%Y %H:%M:%S")
            return timezone.localtime(self.deadline).strftime("%d.%m.%Y")
        return ''

    def get_tree(self,
                 normaltodo_choice='ALL',
                 repetitivetodo_choice='ALL',
                 neverendingtodo_choice='ALL',
                 pipelinetodo_choice='ALL',
                 delta=None,
                 goal_choice='ALL',
                 strategy_choice='ALL',
                 monitor_choice='ALL'):
        data = dict()
        data['name'] = self.name
        data['progress'] = self.progress
        data['pk'] = self.pk
        data['subgoals'] = [goal.get_tree(
            normaltodo_choice,
            repetitivetodo_choice,
            neverendingtodo_choice,
            pipelinetodo_choice,
            delta,
            goal_choice,
            strategy_choice,
            monitor_choice) for goal in list(Goal.get_goals(self.sub_goals.all(), goal_choice))]
        data['strategies'] = [strategy.get_tree(
            normaltodo_choice,
            repetitivetodo_choice,
            neverendingtodo_choice,
            pipelinetodo_choice,
            delta) for strategy in list(Strategy.get_strategies(self.strategies.all(), strategy_choice))]
        data['monitors'] = [monitor.get_tree(
        ) for monitor in list(ProgressMonitor.get_monitors(self.progress_monitors.all(), monitor_choice))]
        return data

    def get_class(self):
        result = min(8, max(1, int(8 * (self.progress + 10) / 100)))
        return result

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

    def get_all_sub_todos(self):
        query = ToDo.objects.none()
        for strategy in self.get_all_sub_strategies():
            query = query | strategy.to_dos.all()
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

    def get_sub_to_dos(self):
        to_dos = []
        for strategy in self.strategies.all():
            to_dos += strategy.get_unfinished_to_dos()
        for goal in self.sub_goals.all():
            to_dos += goal.get_sub_to_dos()
        return to_dos

    def get_progress_calc(self):
        if not self.progress_monitors.exists():
            return self.get_sub_progress()
        return self.get_milestone_progress() + (100 - self.get_milestone_progress()) * self.get_sub_progress() * .008

    def get_milestone_progress(self):
        progress = 0
        weight = 0

        for progress_monitor in self.progress_monitors.all():
            progress += progress_monitor.progress
            weight += progress_monitor.weight

        return progress / weight if weight != 0 else 0

    def get_sub_progress(self):
        progress = 0
        weight = 0

        sub_links = self.sub_links.select_related('sub_goal').all()
        for link in sub_links:
            progress += link.weight * link.progress
            weight += link.weight

        strategies = self.strategies.all()
        for strategy in strategies:
            progress += strategy.weight * strategy.progress
            weight += strategy.weight

        return progress / weight if weight != 0 else 0

    # setters
    def set_starred(self):
        Goal.objects.filter(pk=self.pk).update(is_starred=(not self.is_starred))

    def set_archived(self):
        Goal.objects.filter(pk=self.pk).update(is_archived=(not self.is_archived))

    def reset(self):
        self.progress = self.get_progress_calc()
        self.save()


class ProgressMonitor(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='progress_monitors')
    monitor = models.CharField(max_length=300)
    weight = models.PositiveSmallIntegerField(default=1)
    steps = models.PositiveSmallIntegerField()
    step = models.PositiveSmallIntegerField(default=0, blank=True)
    notes = models.TextField(default='', blank=True)
    is_archived = models.BooleanField(default=False)
    # speed
    progress = models.PositiveSmallIntegerField(default=0, blank=True)

    # general
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.progress = self.get_progress_calc()
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
        # calculate the goals progress
        self.goal.reset()

    class Meta:
        ordering = ('is_archived', 'progress', 'goal')

    def __str__(self):
        return self.monitor

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
        goals = Goal.get_goals_user(user, "ALL")
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
        data['name'] = self.monitor
        data['progress'] = self.progress
        data['pk'] = self.pk
        return data

    def get_progress(self):
        return self.progress

    def get_progress_calc(self):
        return (float(self.step) / float(self.steps)) * 100 if self.steps != 0 else 100


class Link(models.Model):
    master_goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name="sub_links")
    sub_goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name="master_links")
    weight = models.SmallIntegerField(default=1)
    proportion = models.SmallIntegerField(default=100)
    is_archived = models.BooleanField(default=False)
    # speed
    progress = models.PositiveSmallIntegerField(default=0, blank=True)

    # general
    class Meta:
        ordering = ('is_archived', 'progress', 'master_goal')

    def __str__(self):
        return str(self.master_goal) + " --> " + str(self.sub_goal)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
        # reset the master goal progress
        self.master_goal.reset()

    def delete(self, using=None, keep_parents=False):
        master_goal = self.master_goal
        super(Link, self).delete(using=using, keep_parents=keep_parents)
        master_goal.reset()

    # setters
    def reset(self):
        self.progress = self.get_progress_calc()
        self.save()

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

    def get_all_sub_todos(self):
        return self.sub_goal.get_all_sub_todos()

    def get_name(self):
        return self.master_goal.name + ' --> ' + self.sub_goal.name

    def get_progress(self):
        return self.progress

    def get_progress_calc(self):
        return min(Goal.objects.filter(pk=self.sub_goal.id).first().progress * (self.proportion / 100), 100)


class Strategy(models.Model):
    name = models.CharField(max_length=300)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name="strategies")
    weight = models.SmallIntegerField(default=1)
    description = models.TextField(null=True, blank=True)
    rolling = models.DurationField(blank=True, null=True)
    is_archived = models.BooleanField(default=False)
    # speed
    progress = models.PositiveSmallIntegerField(default=0, blank=True)
    # user
    is_starred = models.BooleanField(default=False)

    # general
    class Meta:
        ordering = ('is_archived', 'progress', 'name')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
        # calc goal progress
        self.goal.reset()
        # clean up old stuff. in the past a to do that is set to done or failed was not archived.
        self.to_dos.filter(Q(is_done=True) | Q(has_failed=True), Q(is_archived=False)).update(is_archived=True)

    def __str__(self):
        return str(self.name)

    def delete(self, using=None, keep_parents=False):
        goal = self.goal
        super(Strategy, self).delete(using=using, keep_parents=keep_parents)
        goal.reset()

    # getters
    def get_class(self):
        result = min(8, max(1, int(8 * (self.progress + 10) / 100)))
        return result

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

    def get_tree(self, normaltodo_choice='ALL', repetitivetodo_choice='ALL', neverendingtodo_choice='ALL',
                 pipelinetodo_choice='ALL', delta=None):
        data = dict()
        data['name'] = self.name
        data['pk'] = self.pk
        data['progress'] = self.progress
        strategies = Strategy.objects.filter(pk=self.pk)
        data['normaltodos'] = [todo.get_tree(
        ) for todo in list(ToDo.get_to_dos_strategies(strategies, NormalToDo, normaltodo_choice, delta))]
        data['repetitivetodos'] = [todo.get_tree(
        ) for todo in list(ToDo.get_to_dos_strategies(strategies, RepetitiveToDo, repetitivetodo_choice, delta))]
        data['neverendingtodos'] = [todo.get_tree(
        ) for todo in list(ToDo.get_to_dos_strategies(strategies, NeverEndingToDo, neverendingtodo_choice, delta))]
        data['pipelinetodos'] = [todo.get_tree(
        ) for todo in list(ToDo.get_to_dos_strategies(strategies, PipelineToDo, pipelinetodo_choice, delta))]
        return data

    def get_all_master_objects(self):
        objects = list()
        objects += [self.goal]
        objects += self.goal.get_all_master_objects()
        return objects

    def get_goal(self):
        return self.goal.name if self.goal else ''

    def get_rolling(self):
        if self.rolling is None:
            return ''
        if self.rolling.days == 0:
            rolling = strfdelta(self.rolling, "{hours}h {minutes}min")
        elif self.rolling.days == 1:
            rolling = strfdelta(self.rolling, "{days} day {hours}h {minutes}min")
        else:
            rolling = strfdelta(self.rolling, "{days} days {hours}h {minutes}min")
        return rolling

    def get_progress(self):
        return self.progress

    def get_unfinished_to_dos(self):
        to_dos = list(self.to_dos.filter(td_unfinished_filter()))
        return to_dos

    def get_progress_calc(self):
        progress = 0
        if self.rolling:
            date = timezone.now() - self.rolling
            to_dos = self.to_dos.filter(deadline__gte=date, deadline__lte=timezone.now())
        else:
            to_dos = self.to_dos.all()
        for todo in to_dos:
            if todo.is_done:
                progress += 1
        to_dos_count = to_dos.count()
        progress = progress / to_dos_count * 100 if to_dos_count != 0 else 100
        return progress

    # setters
    def set_starred(self):
        Strategy.objects.filter(pk=self.pk).update(is_starred=(not self.is_starred))

    def set_archived(self):
        Strategy.objects.filter(pk=self.pk).update(is_archived=(not self.is_archived))

    def reset(self):
        self.progress = self.get_progress_calc()
        self.save()


class ToDo(models.Model):
    name = models.CharField(max_length=300)
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE, related_name="to_dos")
    is_done = models.BooleanField(default=False)
    has_failed = models.BooleanField(default=False)
    activate = models.DateTimeField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    is_archived = models.BooleanField(default=False)

    # general
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # set self to archived if done or failed
        if self.is_done or self.has_failed:
            self.is_archived = True
        # save
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
        # update the strategy
        self.strategy.reset()

    class Meta:
        ordering = ('is_archived', 'deadline', 'is_done', 'has_failed', 'activate', 'name')

    def __str__(self):
        return '{}: {} - {}'.format(
            self.name, self.get_activate(accuracy='medium'), self.get_deadline(accuracy='medium'))

    def delete(self, using=None, keep_parents=False):
        strategy = self.strategy
        super(ToDo, self).delete(using=using, keep_parents=keep_parents)
        strategy.reset()

    # getters
    @staticmethod
    def get_to_dos(to_dos, to_do_filter, delta=None, include_archived_to_dos=False):
        if to_do_filter == "ALL":
            to_dos = to_dos
        elif to_do_filter == "ACTIVE":
            to_dos = to_dos.filter(td_active_filter())
        elif to_do_filter == "DELTA":
            to_dos = to_dos.filter(td_delta_filter(delta))
        elif to_do_filter == "OVERDUE":
            to_dos = to_dos.filter(td_overdue_filter())
        elif to_do_filter == "UNFINISHED":
            to_dos = to_dos.filter(td_unfinished_filter())
        elif to_do_filter == "ORANGE":
            to_dos = to_dos.filter(deadline__lt=(F('deadline') - F('activate')) * .2 + timezone.now())
        else:
            to_dos = to_dos.objects.none()

        if not include_archived_to_dos:
            to_dos = to_dos.filter(is_archived=False)

        return to_dos

    @staticmethod
    def get_to_dos_strategies(all_strategies, to_do_class, to_do_filter, delta=None, include_archived_to_dos=False):
        all_to_dos = to_do_class.objects.filter(strategy__in=all_strategies)
        to_dos = ToDo.get_to_dos(all_to_dos, to_do_filter, delta, include_archived_to_dos)
        return to_dos

    @staticmethod
    def get_to_dos_user(user, to_do_class, to_do_filter, delta=None, include_archived_to_dos=False):
        strategies = Strategy.get_strategies_user(user, "ALL")
        all_to_dos = to_do_class.objects.filter(strategy__in=strategies)
        to_dos = ToDo.get_to_dos(all_to_dos, to_do_filter, delta, include_archived_to_dos)
        return to_dos

    def get_all_master_objects(self):
        objects = list()
        objects += [self.strategy]
        objects += self.strategy.get_all_master_objects()
        return objects

    def get_tree(self):
        data = dict()
        data['name'] = self.name
        data['pk'] = self.pk
        data['is_done'] = self.is_done
        data['has_failed'] = self.has_failed
        data['status'] = self.get_to_deadline_time()
        return data

    def get_deadline(self, accuracy='high'):
        if self.deadline:
            if accuracy == 'medium':
                return timezone.localtime(self.deadline).strftime("%d.%m.%Y")
            else:
                return timezone.localtime(self.deadline).strftime("%d.%m.%Y %H:%M")
        return 'none'

    def get_activate(self, accuracy='high'):
        if self.activate:
            if accuracy == 'medium':
                return timezone.localtime(self.activate).strftime("%d.%m.%Y")
            else:
                return timezone.localtime(self.activate).strftime("%d.%m.%Y %H:%M")
        return 'none'

    def get_to_deadline_time(self):
        color = self.get_color()
        delta = self.get_delta()
        return color, delta

    def get_delta(self):
        delta = ''
        if self.is_done:
            delta = 'done'
        elif self.has_failed:
            delta = 'failed'
        elif self.deadline:
            time_delta = self.deadline - timezone.now()
            if abs(time_delta).days == 0:
                delta = strfdelta(abs(time_delta), "{hours}h {minutes}min")
            elif abs(time_delta).days == 1:
                delta = strfdelta(abs(time_delta), "{days} day {hours}h {minutes}min")
            else:
                delta = strfdelta(abs(time_delta), "{days} days {hours}h {minutes}min")
            if time_delta < timedelta():
                delta = "Overdue: " + delta
        return delta

    def get_color(self):
        color = 'blue'
        if self.is_done:
            color = 'green'
        elif self.has_failed:
            color = 'yellow'
        elif self.deadline:
            if self.deadline < timezone.now():
                color = 'red'
            elif self.activate and (self.deadline - timezone.now()) < ((self.deadline - self.activate) * .2):
                color = 'orange'
            else:
                color = 'green'
        return color

    def get_notes(self):
        if self.notes:
            return self.notes
        return ''

    def get_next(self):
        return 'None'

    def get_previous(self):
        return 'None'


class NormalToDo(ToDo):
    pass


class RepetitiveToDo(ToDo):
    duration = models.DurationField()
    previous = models.OneToOneField('self', blank=True, null=True, on_delete=models.SET_NULL, related_name='next')
    repetitions = models.PositiveSmallIntegerField(default=None, null=True)

    # whatever
    def delete(self, using=None, keep_parents=False):
        next_rtd = self.get_next()
        if next_rtd and self.previous:
            next_rtd.previous = self.previous
            self.previous = None
            self.repetitions = 0
            self.save()
            next_rtd.save()
        super(RepetitiveToDo, self).delete(using, keep_parents)

    # getters
    def get_duration(self):
        if abs(self.duration).days == 0:
            duration = strfdelta(self.duration, "{hours}h {minutes}min")
        elif abs(self.duration).days == 1:
            duration = strfdelta(self.duration, "{days} day {hours}h {minutes}min")
        else:
            duration = strfdelta(self.duration, "{days} days {hours}h {minutes}min")
        return duration

    def get_next(self):
        try:
            next_rtd = self.next
        except RepetitiveToDo.next.RelatedObjectDoesNotExist:
            next_rtd = None
        return next_rtd

    def get_previous(self):
        if self.previous:
            return self.previous
        return None

    def get_all_after(self):
        repetitive_to_dos = [self]
        next_repetitive_to_do = self.get_next()
        if next_repetitive_to_do:
            repetitive_to_dos = repetitive_to_dos + next_repetitive_to_do.get_all_after()
        return repetitive_to_dos
        # this code may throw a parser stack overflow
        # q = RepetitiveToDo.objects.filter(pk=self.pk)
        # next_rtd = self.get_next()
        # if next_rtd:
        #     q = q | next_rtd.get_all_after()
        # return q

    def get_all_before(self):
        q = RepetitiveToDo.objects.filter(pk=self.pk)
        if self.previous:
            q = q | self.previous.get_all_before()
        return q

    # generate
    def generate_next(self):
        next_deadline = self.deadline + self.duration
        if self.repetitions <= 0:
            return
        next_activate = self.activate + self.duration
        repetitions = self.repetitions - 1
        RepetitiveToDo.objects.create(name=self.name, strategy=self.strategy, previous=self, deadline=next_deadline,
                                      activate=next_activate, repetitions=repetitions, duration=self.duration)


class NeverEndingToDo(ToDo):
    duration = models.DurationField()
    previous = models.ForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL, related_name="next")

    # getters
    def get_duration(self):
        if abs(self.duration).days == 0:
            duration = strfdelta(self.duration, "{hours}h {minutes}min")
        elif abs(self.duration).days == 1:
            duration = strfdelta(self.duration, "{days} day {hours}h {minutes}min")
        else:
            duration = strfdelta(self.duration, "{days} days {hours}h {minutes}min")
        return duration

    def get_next(self):
        return self.next.first()

    def get_previous(self):
        return self.previous

    # generate
    def generate_next(self):
        now = timezone.now()
        next_deadline = now + self.duration
        next_activate = now
        NeverEndingToDo.objects.create(name=self.name, strategy=self.strategy, previous=self, deadline=next_deadline,
                                       activate=next_activate, duration=self.duration)


class PipelineToDo(ToDo):
    previous = models.ForeignKey(ToDo, null=True, on_delete=models.SET_NULL, related_name='pipeline_to_dos')

    # getters
    def get_next(self):
        return ', '.join([to_do.name for to_do in self.pipeline_to_dos.all()])

    def get_previous(self):
        return self.previous
