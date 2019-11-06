from django.db.models import signals
from django.shortcuts import reverse
from django.db.models import Q, F
from django.utils import timezone
from django.db import models

from mastergoal.users.models import CustomUser
from mastergoal.core.utils import strfdelta

from datetime import timedelta


def td_all_filter():
    return Q()


def td_unfinished_filter():
    return Q(Q(activate__lte=timezone.now()) | Q(activate=None), is_done=False, has_failed=False)


def td_active_filter():
    return Q(activate__lte=timezone.now(), is_done=False, has_failed=False)


def td_overdue_filter():
    return Q(deadline__lte=timezone.now(), is_done=False, has_failed=False)


def td_related_filter(strategies):
    return Q(strategy__in=strategies, is_done=False, has_failed=False)


def td_delta_filter(delta):
    return Q(deadline__lte=timezone.now() + delta, activate__lte=timezone.now(), is_done=False, has_failed=False)


def td_orange_filter():
    return Q(activate__lte=timezone.now(), is_done=False, has_failed=False)


def td_none_filter():
    return Q(pk=None)


def g_all_filter():
    return Q()


def g_active_filter():
    return Q(is_archived=False, progress__lt=100)


def g_star_filter():
    return Q(is_starred=True)


def g_unreached_filter():
    return Q(progress__lt=100, archived=False)


def g_achieved_filter():
    return Q(progress__gte=100)


def g_archive_filter():
    return Q(is_archived=True)


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


def m_related_filter(goals):
    return Q(goal__in=goals)


def m_none_filter():
    return Q(pk=None)


def l_all_filter():
    return Q()


def l_related_filter(goals):
    return Q(Q(master_goal__in=goals) | Q(sub_goal__in=goals))


def l_xrelated_filter(goals):
    return Q(master_goal__in=goals, sub_goal__in=goals)


def l_none_filter():
    return Q(pk=None)


def s_all_filter():
    return Q()


def s_star_filter():
    return Q(is_starred=True)


def s_related_filter(goals):
    return Q(goal__in=goals)


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

    # whatever
    class Meta:
        ordering = ('progress', 'deadline', 'name')

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        master_goals = self.master_goals.all()
        super(Goal, self).delete(using=using, keep_parents=keep_parents)
        [master_goal.calc() for master_goal in master_goals]

    # get
    @staticmethod
    def get_goals(goals, choice):
        if choice == "ALL":
            goals = goals.filter(g_all_filter())
        elif choice == 'ACTIVE':
            goals = goals.filter(g_active_filter())
        elif choice == "STAR":
            goals = goals.filter(g_star_filter())
        elif choice == "UNREACHED":
            goals = goals.exclude(g_unreached_filter())
        elif choice == "ACHIEVED":
            goals = goals.filter(g_achieved_filter())
        elif choice == "DEPTH" and False:
            goals = goals.filter(g_depth_filter())
        elif choice == 'ARCHIVE':
            goals = goals.filter(g_archive_filter())
        else:
            goals = goals.filter(g_none_filter())
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
                 multipletodo_choice='ALL',
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
            multipletodo_choice,
            delta,
            goal_choice,
            strategy_choice,
            monitor_choice) for goal in list(Goal.get_goals(self.sub_goals.all(), goal_choice))]
        data['strategies'] = [strategy.get_tree(
            normaltodo_choice,
            repetitivetodo_choice,
            neverendingtodo_choice,
            pipelinetodo_choice,
            multipletodo_choice,
            delta) for strategy in list(Strategy.get_strategies(self.strategies.all(), strategy_choice))]
        data['monitors'] = [monitor.get_tree(
            ) for monitor in list(ProgressMonitor.get_monitors(self.progress_monitors.all(), monitor_choice))]
        return data

    def get_tree_html(self):
        sub_goals = ''.join([goal.get_tree_html() for goal in self.sub_goals.exclude(progress=100, is_archived=True)])
        sub_goals_tree = '<ul class="tree--nested">{}</ul>'.format(sub_goals)
        sub_strategies = ''.join([strategy.get_tree_html() for strategy in self.strategies.exclude(progress=100)])
        sub_strategies_tree = '<ul class="tree--nested">{}</ul>'.format(sub_strategies)
        sub_progress_monitors = ''.join([pm.get_tree_html() for pm in self.progress_monitors.exclude(progress=100)])
        sub_progress_monitors_tree = '<ul class="tree--nested">{}</ul>'.format(sub_progress_monitors)
        html = '<li class="tree--li">' \
               '<span class="tree--caret">' \
               '<span class="tree--caret--name">' \
               '<span class="tree--caret--arrow">&#8611;</span>' \
               ' {}</span>' \
               '<span class="blue-badge">{} %</span>' \
               '<a class="adminator-href-button" href="{}">Open</a>' \
               '</span>' \
               '{}{}{}</li>'
        item = html.format(self.name, self.progress, reverse('goals:goal', args=[self.pk]), sub_progress_monitors_tree,
                           sub_goals_tree, sub_strategies_tree)
        return item

    def get_class(self):
        result = min(8, max(1, int(8 * (self.progress + 10) / 100)))
        return result

    def get_all_subgoals(self):
        query = self.sub_goals.all()
        for goal in self.sub_goals.all():
            query = query | goal.get_all_subgoals()
        return query

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

    # set
    def set_starred(self):
        Goal.objects.filter(pk=self.pk).update(is_starred=(not self.is_starred))

    # calc
    def calc(self):
        self.progress = self.calc_progress()
        self.save()
        for link in self.master_links.all():
            link.calc()

    def calc_progress(self):
        if not self.progress_monitors.exists():
            return self.calc_sub_progress()
        return self.calc_milestone_progress() + (100 - self.calc_milestone_progress()) * self.calc_sub_progress() * .008

    def calc_milestone_progress(self):
        progress = 0
        weight = 0

        for progress_monitor in self.progress_monitors.all():
            progress += progress_monitor.progress
            weight += progress_monitor.weight

        return progress / weight if weight != 0 else 0

    def calc_sub_progress(self):
        progress = 0
        weight = 0

        sub_links = self.sub_links.select_related('sub_goal').all()
        for link in sub_links:
            # link.calc()
            progress += link.weight * link.progress
            weight += link.weight

        strategies = self.strategies.all()
        for strategy in strategies:
            progress += strategy.weight * strategy.progress
            weight += strategy.weight

        return progress / weight if weight != 0 else 0


class ProgressMonitor(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='progress_monitors')
    monitor = models.CharField(max_length=300)
    weight = models.PositiveSmallIntegerField(default=1)
    steps = models.PositiveSmallIntegerField()
    step = models.PositiveSmallIntegerField(default=0, blank=True)
    notes = models.TextField(default='', blank=True)
    # speed
    progress = models.PositiveSmallIntegerField(default=0, blank=True)

    class Meta:
        ordering = ('progress', 'goal')

    def __str__(self):
        return self.monitor

    def delete(self, using=None, keep_parents=False):
        goal = self.goal
        super(ProgressMonitor, self).delete(using=using, keep_parents=keep_parents)
        goal.calc()

    # get
    @staticmethod
    def get_monitors(monitors, choice, goals=None):
        if choice == "ALL":
            monitors = monitors.filter(m_all_filter())
        elif choice == "UNREACHED":
            monitors = monitors.filter(m_unreached_filter())
        elif choice == "LOADED":
            monitors = monitors.filter(m_loaded_filter())
        elif choice == "RELATED":
            monitors = monitors.filter(m_related_filter(goals))
        else:
            monitors = monitors.filter(m_none_filter())
        return monitors

    def get_tree(self):
        data = dict()
        data['name'] = self.monitor
        data['progress'] = self.progress
        data['pk'] = self.pk
        return data

    def get_tree_html(self):
        html = '<li class="tree--li">' \
               '<div class="tree--caret">' \
               '<span class="tree--caret--name">' \
               '<span class="tree--caret--arrow">&#8613;</span>' \
               ' {}</span>' \
               '<span class="blue-badge">{} %</span>' \
               '<a class="adminator-href-button" href="{}">Open</a>' \
               '</div>' \
               '</li>'
        item = html.format(self.monitor, self.progress, reverse('goals:progress_monitor', args=[self.pk]))
        return item

    def get_progress(self):
        return self.progress

    # calc
    def calc(self):
        self.progress = self.calc_progress()
        self.save()
        self.goal.calc()

    def calc_progress(self):
        return (float(self.step) / float(self.steps)) * 100 if self.steps != 0 else 100


class Link(models.Model):
    master_goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name="sub_links")
    sub_goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name="master_links")
    weight = models.SmallIntegerField(default=1)
    proportion = models.SmallIntegerField(default=100)
    # speed
    progress = models.PositiveSmallIntegerField(default=0, blank=True)

    # whatever
    class Meta:
        ordering = ('progress', 'master_goal')

    def __str__(self):
        return str(self.master_goal) + " --> " + str(self.sub_goal)

    def delete(self, using=None, keep_parents=False):
        master_goal = self.master_goal
        super(Link, self).delete(using=using, keep_parents=keep_parents)
        master_goal.calc()

    # get
    @staticmethod
    def get_links(links, choice, goals=None):
        if choice == "ALL":
            links = links.filter(l_all_filter())
        elif choice == "RELATED":
            links = links.filter(l_related_filter(goals))
        elif choice == "XRELATED":
            links = links.filter(l_xrelated_filter(goals))
        else:
            links = links.filter(l_none_filter())
        return links

    def get_name(self):
        return self.master_goal.name + ' --> ' + self.sub_goal.name

    def get_progress(self):
        return self.progress

    # calc
    def calc(self):
        self.progress = self.calc_progress()
        self.save()
        self.master_goal.calc()

    def calc_progress(self):
        return min(self.sub_goal.progress * (100 / self.proportion), 100)


class Strategy(models.Model):
    name = models.CharField(max_length=300)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name="strategies")
    weight = models.SmallIntegerField(default=1)
    description = models.TextField(null=True, blank=True)
    rolling = models.DurationField(blank=True, null=True)
    # speed
    progress = models.PositiveSmallIntegerField(default=0, blank=True)
    # user
    is_starred = models.BooleanField(default=False)

    # whatever
    class Meta:
        ordering = ('progress', 'name')

    def __str__(self):
        return str(self.name)

    def delete(self, using=None, keep_parents=False):
        goal = self.goal
        super(Strategy, self).delete(using=using, keep_parents=keep_parents)
        goal.calc()

    # get
    @staticmethod
    def get_strategies(strategies, choice, goals=None):
        if choice == "ALL":
            strategies = strategies.filter(s_all_filter())
        elif choice == "STAR":
            strategies = strategies.filter(s_star_filter())
        elif choice == "RELATED":
            strategies = strategies.filter(s_related_filter(goals))
        else:
            strategies = strategies.filter(s_none_filter())
        return strategies

    def get_tree(self, normaltodo_choice='ALL', repetitivetodo_choice='ALL', neverendingtodo_choice='ALL',
                 pipelinetodo_choice='ALL', multipletodo_choice='ALL', delta=None):
        data = dict()
        data['name'] = self.name
        data['pk'] = self.pk
        data['progress'] = self.progress
        strategies = Strategy.objects.filter(pk=self.pk)
        data['normaltodos'] = [todo.get_tree(
            ) for todo in list(ToDo.get_to_dos(strategies, ToDo, normaltodo_choice, delta))]
        data['repetitivetodos'] = [todo.get_tree(
            ) for todo in list(ToDo.get_to_dos(strategies, RepetitiveToDo, repetitivetodo_choice, delta))]
        data['neverendingtodos'] = [todo.get_tree(
            ) for todo in list(ToDo.get_to_dos(strategies, NeverEndingToDo, neverendingtodo_choice, delta))]
        data['pipelinetodos'] = [todo.get_tree(
            ) for todo in list(ToDo.get_to_dos(strategies, PipelineToDo, pipelinetodo_choice, delta))]
        data['multipletodos'] = [todo.get_tree(
            ) for todo in list(ToDo.get_to_dos(strategies, MultipleToDo, multipletodo_choice, delta))]
        return data

    def get_tree_html(self):
        to_dos_filter = Q(is_done=False, has_failed=False)
        to_dos = ''.join([to_do.get_tree_html() for to_do in self.to_dos.filter(to_dos_filter)])
        to_dos_tree = '<ul class="tree--nested">{}</ul>'.format(to_dos)
        html = '<li class="tree--li">' \
               '<span class="tree--caret">' \
               '<span class="tree--caret--name">' \
               '<span class="tree--caret--arrow">&#8605;</span>' \
               ' {}</span>' \
               '<span class="blue-badge">{} %</span>' \
               '<a class="adminator-href-button" href="{}">Open</a>' \
               '</span>' \
               '{}</li>'
        item = html.format(self.name, self.progress, reverse('goals:strategy', args=[self.pk]),
                           to_dos_tree)
        return item

    def get_goal(self):
        return self.goal.name if self.goal else ''

    def get_rolling(self):
        if self.rolling is None:
            return ''
        if abs(self.rolling).days == 0:
            rolling = strfdelta(self.rolling, "{hours}h {minutes}min")
        elif abs(self.rolling).days == 1:
            rolling = strfdelta(self.rolling, "{days} day {hours}h {minutes}min")
        else:
            rolling = strfdelta(self.rolling, "{days} days {hours}h {minutes}min")
        return rolling

    def get_progress(self):
        return self.progress

    def get_unfinished_to_dos(self):
        to_dos = list(self.to_dos.filter(td_unfinished_filter()))
        return to_dos

    # set
    def set_starred(self):
        Strategy.objects.filter(pk=self.pk).update(is_starred=(not self.is_starred))

    # calc
    def calc(self):
        self.progress = self.calc_progress()
        self.save()
        self.goal.calc()

    def calc_progress(self):
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
        return progress / to_dos_count * 100 if to_dos_count != 0 else 0


class ToDo(models.Model):
    name = models.CharField(max_length=300)
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE, related_name="to_dos")
    is_done = models.BooleanField(default=False)
    has_failed = models.BooleanField(default=False)
    activate = models.DateTimeField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    # whatever
    class Meta:
        ordering = ('is_done', 'has_failed', 'deadline', 'activate', 'name')

    def __str__(self):
        return str(self.name) + ": " + self.get_activate(accuracy='medium') + " - " + self.get_deadline(accuracy='medium')

    def delete(self, using=None, keep_parents=False):
        strategy = self.strategy
        super(ToDo, self).delete(using=using, keep_parents=keep_parents)
        strategy.calc()

    # getters
    @staticmethod
    def get_to_dos(all_strategies, to_do_class, to_dos_filter, delta=None, strategies=None):
        all_to_dos = to_do_class.objects.filter(strategy__in=all_strategies)

        if to_do_class is ToDo:
            all_to_dos = to_do_class.objects.filter(strategy__in=all_strategies) \
                .exclude(pk__in=RepetitiveToDo.objects.filter(strategy__in=all_strategies)) \
                .exclude(pk__in=NeverEndingToDo.objects.filter(strategy__in=all_strategies)) \
                .exclude(pk__in=MultipleToDo.objects.filter(strategy__in=all_strategies)) \
                .exclude(pk__in=PipelineToDo.objects.filter(strategy__in=all_strategies))

        if to_dos_filter == "ALL":
            to_dos = all_to_dos
        elif to_dos_filter == "ACTIVE":
            to_dos = all_to_dos.filter(td_active_filter())
        elif to_dos_filter == "DELTA":
            to_dos = all_to_dos.filter(td_delta_filter(delta))
        elif to_dos_filter == "OVERDUE":
            to_dos = all_to_dos.filter(td_overdue_filter())
        elif to_dos_filter == "UNFINISHED":
            to_dos = all_to_dos.filter(td_unfinished_filter())
        elif to_dos_filter == "ORANGE":
            to_dos = all_to_dos.filter(deadline__lt=(F('deadline') - F('activate')) * .2 + timezone.now())
        else:
            to_dos = to_do_class.objects.none()
        to_dos = to_dos.order_by('deadline')

        return to_dos

    def get_tree(self):
        data = dict()
        data['name'] = self.name
        data['pk'] = self.pk
        data['is_done'] = self.is_done
        data['has_failed'] = self.has_failed
        data['deadline'] = self.get_deadline()
        return data

    def get_tree_html(self):
        html = '<li class="tree--li">' \
               '<span class="tree--caret">' \
               '<span class="tree--caret--name">' \
               '<span class="tree--caret--arrow">&#8623;</span>' \
               ' {}</span>' \
               '<a class="adminator-href-button" href="{}">Open</a>' \
               '</span>' \
               '</li>'
        item = html.format(self.name, reverse('goals:to_do', args=[self.pk]))
        return item

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

    # calc
    def calc(self):
        self.strategy.calc()


class RepetitiveToDo(ToDo):
    end_day = models.DateTimeField()
    duration = models.DurationField()
    previous = models.OneToOneField('self', blank=True, null=True, on_delete=models.SET_NULL, related_name='next')
    trash = models.BooleanField(default=False, editable=False)

    # whatever
    def delete(self, using=None, keep_parents=False):
        next_rtd = self.get_next()
        if next_rtd and self.previous:
            next_rtd.previous = self.previous
            self.previous = None
            self.trash = True
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
        q = RepetitiveToDo.objects.filter(pk=self.pk)
        next_rtd = self.get_next()
        if next_rtd:
            q = q | next_rtd.get_all_after()
        return q

    def get_all_before(self):
        q = RepetitiveToDo.objects.filter(pk=self.pk)
        if self.previous:
            q = q | self.previous.get_all_before()
        return q

    # generate
    def generate_next(self):
        next_deadline = self.deadline + self.duration
        if self.end_day and next_deadline > self.end_day:
            return
        next_activate = self.activate + self.duration
        RepetitiveToDo.objects.create(name=self.name, strategy=self.strategy, previous=self, deadline=next_deadline,
                                      activate=next_activate, end_day=self.end_day, duration=self.duration)


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


class MultipleToDo(ToDo):
    pass


# signals
def post_save_target(sender, instance, **kwargs):
    if sender is ToDo:
        if instance.pipeline_to_dos.exists() and instance.is_done:
            instance.pipeline_to_dos.update(activate=timezone.now())
    if sender is RepetitiveToDo:
        if not instance.trash:
            if not instance.get_next():
                instance.generate_next()
    elif sender is NeverEndingToDo:
        if (instance.is_done or instance.has_failed) and not instance.next.all().exists():
            instance.generate_next()


signals.post_save.connect(post_save_target, sender=ToDo)
signals.post_save.connect(post_save_target, sender=RepetitiveToDo)
signals.post_save.connect(post_save_target, sender=NeverEndingToDo)
