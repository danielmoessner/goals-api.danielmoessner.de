from apps.users.models import CustomUser
from django.utils.html import strip_tags
from django.db import models
from tinymce import HTMLField


class Note(models.Model):
    user = models.ForeignKey(CustomUser, related_name='notes', on_delete=models.CASCADE)
    content = HTMLField()
    created = models.DateTimeField(auto_created=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['created']

    @property
    def name(self):
        return strip_tags(self.content.split('</', 1)[0])

    def __str__(self):
        return strip_tags(self.content.split('</', 1)[0])
