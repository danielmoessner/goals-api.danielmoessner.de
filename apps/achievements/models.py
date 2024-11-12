from django.db import models

from apps.users.models import CustomUser


class Achievement(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField()
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Achievement"
        verbose_name_plural = "Achievements"
        ordering = ["-date"]

    def __str__(self):
        return "{}".format(self.title)

    @property
    def date_str(self):
        return self.date.strftime("%d.%m.%Y")
