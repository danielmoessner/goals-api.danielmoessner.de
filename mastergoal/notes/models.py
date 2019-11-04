from django.utils.html import strip_tags
from django.db import models

from mastergoal.users.models import CustomUser

from tinymce import HTMLField


class Note(models.Model):
    user = models.ForeignKey(CustomUser, related_name='notes', on_delete=models.CASCADE)
    content = HTMLField()

    def __str__(self):
        return strip_tags(self.content.split('\n', 1)[0][:50])