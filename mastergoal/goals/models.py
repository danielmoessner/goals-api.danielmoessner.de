from django.db.models import signals
from django.shortcuts import reverse
from django.db.models import Q
from django.utils import timezone
from django.db import models

from mastergoal.users.models import CustomUser
from mastergoal.core.utils import strfdelta

from datetime import timedelta


class Goal(models.Model):
    user = models.ForeignKey(CustomUser, related_name='goals', on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    why = models.TextField(blank=True, null=True)
    impact = models.TextField(blank=True, null=True)
    deadline = models.DateTimeField(null=True, blank=True)
    sub_goals = models.ManyToManyField(to='self', through='Link', symmetrical=False, related_name='master_goals')
    # speed
    progress = models.PositiveSmallIntegerField(default=0, blank=True)
    # user
    is_starred = models.BooleanField(default=False)

    # whatever
    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        master_goals = self.master_goals.all()
        super(Goal, self).delete(using=using, keep_parents=keep_parents)
        [master_goal.calc() for master_goal in master_goals]

    # get
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
        return 'no-deadline'

    def get_tree_html(self):
        sub_goals = ''.join([goal.get_tree_html() for goal in self.sub_goals.exclude(progress=100)])
        sub_goals_tree = '<ul class="tree--nested">{}</ul>'.format(sub_goals)
        sub_strategies = ''.join([strategy.get_tree_html() for strategy in self.strategies.all()])
        sub_strategies_tree = '<ul class="tree--nested">{}</ul>'.format(sub_strategies)
        sub_progress_monitors = ''.join([pm.get_tree_html() for pm in self.progress_monitors.all()])
        sub_progress_monitors_tree = '<ul class="tree--nested">{}</ul>'.format(sub_progress_monitors)
        item = '<li><span class="tree--caret" href="{}">{}</span>{}{}{}</li>'\
            .format(reverse('goals:goal', args=[self.pk]),
                    self.name,
                    sub_progress_monitors_tree,
                    sub_strategies_tree,
                    sub_goals_tree)
        return item

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

    def __str__(self):
        return self.monitor

    def delete(self, using=None, keep_parents=False):
        goal = self.goal
        super(ProgressMonitor, self).delete(using=using, keep_parents=keep_parents)
        goal.calc()

    # get
    def get_tree_html(self):
        item = '<li><span class="tree--caret tree--caret-red tree--caret-round" href="{}">{}</span>{}</li>'\
            .format(reverse('goals:progress_monitor', args=[self.pk]), self.monitor, '')
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
    def __str__(self):
        return str(self.master_goal) + " --> " + str(self.sub_goal)

    def delete(self, using=None, keep_parents=False):
        master_goal = self.master_goal
        super(Link, self).delete(using=using, keep_parents=keep_parents)
        master_goal.calc()

    # get
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
    def __str__(self):
        return str(self.name)

    def delete(self, using=None, keep_parents=False):
        goal = self.goal
        super(Strategy, self).delete(using=using, keep_parents=keep_parents)
        goal.calc()

    # get
    def get_tree_html(self):
        to_dos_filter = Q(is_done=False, has_failed=False)
        to_dos = ''.join([to_do.get_tree_html() for to_do in self.to_dos.filter(to_dos_filter)])
        to_dos_tree = '<ul class="tree--nested">{}</ul>'.format(to_dos)
        item = '<li><span class="tree--caret tree--caret-blue" href="{}">{}</span>{}</li>'\
            .format(reverse('goals:strategy', args=[self.pk]),
                    self.name,
                    to_dos_tree)
        return item

    def get_goal(self):
        return self.goal.name if self.goal else ''

    def get_deadline(self):
        return 'no-deadline'

    def get_progress(self):
        return self.progress

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
    def __str__(self):
        return str(self.name) + ": " + self.get_activate(accuracy='medium') + " - " + self.get_deadline(accuracy='medium')

    def delete(self, using=None, keep_parents=False):
        strategy = self.strategy
        super(ToDo, self).delete(using=using, keep_parents=keep_parents)
        strategy.calc()

    # getters
    def get_tree_html(self):
        item = '<li><span class="tree--caret tree--caret-green tree--caret-round">{}</span></li>'.format(self.name)
        return item

    def get_deadline(self, accuracy='high'):
        if self.deadline:
            if accuracy == 'medium':
                return timezone.localtime(self.deadline).strftime("%d.%m.%Y")
            else:
                return timezone.localtime(self.deadline).strftime("%d.%m.%Y %H:%M")
        return 'no-deadline'

    def get_activate(self, accuracy='high'):
        if self.deadline:
            if accuracy == 'medium':
                return timezone.localtime(self.activate).strftime("%d.%m.%Y")
            else:
                return timezone.localtime(self.activate).strftime("%d.%m.%Y %H:%M")
        return 'no-deadline'

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
    previous = models.ForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL, related_name="next")

    # whatever
    def delete(self, using=None, keep_parents=False):
        next_to_do = self.next.first()
        if next_to_do:
            next_to_do.previous = self.previous
            next_to_do.save()
        super(RepetitiveToDo, self).delete(using, keep_parents)

    # getters
    def get_next(self):
        return self.next.first()

    def get_previous(self):
        return self.previous

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
        if not instance.next.all().exists():
            instance.generate_next()
    elif sender is NeverEndingToDo:
        if (instance.is_done or instance.has_failed) and not instance.next.all().exists():
            instance.generate_next()


signals.post_save.connect(post_save_target, sender=ToDo)
signals.post_save.connect(post_save_target, sender=RepetitiveToDo)
signals.post_save.connect(post_save_target, sender=NeverEndingToDo)
