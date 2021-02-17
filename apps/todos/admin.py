from django.contrib import admin

from .models import NormalToDo, NeverEndingToDo, PipelineToDo, RepetitiveToDo

admin.site.register(NormalToDo)
admin.site.register(NeverEndingToDo)
admin.site.register(PipelineToDo)
admin.site.register(RepetitiveToDo)
