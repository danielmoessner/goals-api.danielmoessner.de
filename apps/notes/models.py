from apps.users.models import CustomUser
from django.utils.html import strip_tags
from django.db import models
from tinymce.models import HTMLField


class Note(models.Model):
    user = models.ForeignKey(CustomUser, related_name='notes', on_delete=models.CASCADE)
    content = HTMLField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['updated']

    @property
    def name(self):
        return strip_tags(self.content.split('</', 1)[0])
    
    @property
    def last_update_str(self):
        return self.updated.strftime("%d.%m.%Y")

    def __str__(self):
        return self.name
