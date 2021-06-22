from django.core.exceptions import ObjectDoesNotExist
from apps.users.models import CustomUser
from django.utils import timezone
from django.db import models
from datetime import timedelta


class ToDo(models.Model):
    name = models.CharField(max_length=300)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="to_dos")
    activate = models.DateTimeField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    completed = models.DateTimeField(null=True, blank=True)
    status_choices = (
        ('ACTIVE', 'Active'),
        ('DONE', 'Done'),
        ('FAILED', 'Failed')
    )
    status = models.CharField(choices=status_choices, max_length=20, default='ACTIVE')
    created = models.DateTimeField(auto_created=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    # general
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # set completed
        if self.completed is None and (self.status == 'DONE' or self.status == 'FAILED'):
            self.completed = timezone.now()
        if self.status == 'ACTIVE':
            self.completed = None
        # activate pipeline to dos
        if self.status == 'DONE':
            self.pipeline_to_dos.filter(activate=None).update(activate=timezone.now())
        elif self.status == 'FAILED':
            self.pipeline_to_dos.filter(activate=None).update(status='FAILED', activate=timezone.now())
        # save
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    class Meta:
        ordering = ('status', 'name', 'deadline', 'activate')

    def __str__(self):
        return '{}: {} - {}'.format(
            self.name, self.get_activate(accuracy='medium'), self.get_deadline(accuracy='medium'))

    # getters
    @staticmethod
    def get_to_dos(to_dos, include_old_todos=False):
        if not include_old_todos:
            to_dos = to_dos.exclude(completed__lt=timezone.now() - timedelta(days=40))
        return to_dos

    @staticmethod
    def get_to_dos_user(user, to_do_class):
        all_to_dos = to_do_class.objects.filter(user=user)
        to_dos = ToDo.get_to_dos(all_to_dos, include_old_todos=user.show_old_todos)
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


class NormalToDo(ToDo):
    pass


class RepetitiveToDo(ToDo):
    duration = models.DurationField()
    previous = models.OneToOneField('self', blank=True, null=True, on_delete=models.SET_NULL, related_name='next')
    repetitions = models.PositiveSmallIntegerField()
    blocked = models.BooleanField(default=False)

    def __str__(self):
        return '{} {}'.format(super().__str__(), self.repetitions)

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
    def get_next(self):
        try:
            next_rtd = self.next
        except RepetitiveToDo.next.RelatedObjectDoesNotExist:
            next_rtd = None
        return next_rtd

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

    # getters
    @property
    def next_todo(self):
        try:
            return self.next
        except ObjectDoesNotExist:
            return None

    # generate
    def generate_next(self):
        now = timezone.now()
        next_activate = now + self.duration
        NeverEndingToDo.objects.create(name=self.name, user=self.user, previous=self,
                                       activate=next_activate, duration=self.duration)


class PipelineToDo(ToDo):
    previous = models.ForeignKey(ToDo, null=True, on_delete=models.SET_NULL, related_name='pipeline_to_dos')
