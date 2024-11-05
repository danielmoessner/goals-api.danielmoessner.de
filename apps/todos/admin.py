from apps.todos.models import NormalToDo, NeverEndingToDo, PipelineToDo, RepetitiveToDo
from django.contrib import admin

admin.site.register(NormalToDo)
admin.site.register(NeverEndingToDo)
admin.site.register(PipelineToDo)
admin.site.register(RepetitiveToDo)
