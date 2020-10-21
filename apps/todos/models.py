from django.core.serializers.json import DjangoJSONEncoder
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from apps.users.models import CustomUser
from django.db.models import Q, F
from django.utils import timezone
from django.urls import reverse_lazy
from django.db import models
import json


def td_all_filter():
    return Q()


def td_unfinished_filter():
    return Q(status='ACTIVE')


def td_active_filter():
    return Q(activate__lte=timezone.now(), status='ACTIVE')


def td_overdue_filter():
    return Q(deadline__lte=timezone.now(), status='ACTIVE')


def td_delta_filter(delta):
    return Q(deadline__lte=timezone.now() + delta, activate__lte=timezone.now(), status='ACTIVE')


def td_orange_filter():
    return Q(activate__lte=timezone.now(), status='ACTIVE')


def td_none_filter():
    return Q(pk=None)


class ToDo(models.Model):
    name = models.CharField(max_length=300)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="to_dos")
    activate = models.DateTimeField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    is_archived = models.BooleanField(default=False)
    completed = models.DateTimeField(null=True, blank=True)
    status_choices = (
        ('ACTIVE', 'Active'),
        ('DONE', 'Done'),
        ('FAILED', 'Failed')
    )
    status = models.CharField(choices=status_choices, max_length=20, default='ACTIVE')

    # general
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # set self to archived if done or failed
        # if not self.is_archived and (self.status == 'DONE' or self.status == 'FAILED'):
        #     self.is_archived = True
        if self.completed is None and (self.status == 'DONE' or self.status == 'FAILED'):
            self.is_archived = True
            self.completed = timezone.now()
        if self.status == 'ACTIVE':
            self.completed = None
        # activate pipeline to dos
        if self.status == 'DONE':
            self.pipeline_to_dos.update(activate=timezone.now())
        else:
            self.pipeline_to_dos.update(activate=None)
        # save
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    class Meta:
        ordering = ('is_archived', 'deadline', 'status', 'activate', 'name')

    def __str__(self):
        return '{}: {} - {}'.format(
            self.name, self.get_activate(accuracy='medium'), self.get_deadline(accuracy='medium'))

    # getters
    def get_json(self):
        dict_obj = model_to_dict(self)
        json_obj = json.dumps(dict_obj, cls=DjangoJSONEncoder)
        return json_obj

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
    def get_to_dos_user(user, to_do_class, to_do_filter, delta=None, include_archived_to_dos=False):
        all_to_dos = to_do_class.objects.filter(user=user)
        to_dos = ToDo.get_to_dos(all_to_dos, to_do_filter, delta, include_archived_to_dos)
        return to_dos

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
        @property
        def form_url(self):
            return reverse_lazy('todos:normaltodo-form', args=[self.pk])


class RepetitiveToDo(ToDo):
    duration = models.DurationField()
    previous = models.OneToOneField('self', blank=True, null=True, on_delete=models.SET_NULL, related_name='next')
    repetitions = models.PositiveSmallIntegerField(default=None, null=True)

    @property
    def form_url(self):
        return reverse_lazy('todos:repetitivetodo-form', args=[self.pk])

    def save(self, *args, **kwargs):
        super(RepetitiveToDo, self).save(*args, **kwargs)
        if self.repetitions > 0 and self.get_next() is None:
            self.generate_next()

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
    def get_json(self):
        dict_obj = model_to_dict(self)
        json_obj = json.dumps(dict_obj, cls=DjangoJSONEncoder)
        return json_obj

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
        RepetitiveToDo.objects.create(name=self.name, user=self.user, previous=self, deadline=next_deadline,
                                      activate=next_activate, repetitions=repetitions, duration=self.duration)


class NeverEndingToDo(ToDo):
    duration = models.DurationField()
    previous = models.OneToOneField('self', blank=True, null=True, on_delete=models.SET_NULL, related_name='next')
    blocked = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        if self.previous is not None:
            self.previous.blocked = True
            self.previous.save()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if (self.status == 'DONE' or self.status == 'FAILED') and self.next_todo is None and self.blocked is False:
            self.generate_next()

    @property
    def next_todo(self):
        try:
            return self.next
        except ObjectDoesNotExist:
            return None

    @property
    def form_url(self):
        return reverse_lazy('todos:neverendingtodo-form', args=[self.pk])

    # getters
    def get_next(self):
        return self.next_todo

    def get_previous(self):
        return self.previous

    # generate
    def generate_next(self):
        now = timezone.now()
        next_deadline = now + self.duration
        next_activate = now
        NeverEndingToDo.objects.create(name=self.name, user=self.user, previous=self, deadline=next_deadline,
                                       activate=next_activate, duration=self.duration)


class PipelineToDo(ToDo):
    previous = models.ForeignKey(ToDo, null=True, on_delete=models.SET_NULL, related_name='pipeline_to_dos')

    @property
    def form_url(self):
        return reverse_lazy('todos:pipelinetodo-form', args=[self.pk])

    # getters
    def get_update_url(self):
        return reverse_lazy('todos:pipeline_to_do_edit', args=[self.pk])

    def get_json(self):
        dict_obj = model_to_dict(self)
        json_obj = json.dumps(dict_obj, cls=DjangoJSONEncoder)
        return json_obj

    def get_next(self):
        return ', '.join([to_do.name for to_do in self.pipeline_to_dos.all()])

    def get_previous(self):
        return self.previous
