from apps.users.models import CustomUser
from django.db import models
from tinymce.models import HTMLField


class Story(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='stories')
    what_is = HTMLField(blank=True)
    what_should_be = HTMLField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        verbose_name = 'Story'
        verbose_name_plural = 'Stories'

    def __str__(self):
        return '{}: {}'.format(self.created.strftime('%Y-%m-%d'), self.user.email)

