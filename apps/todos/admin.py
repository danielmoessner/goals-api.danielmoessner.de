from apps.todos.models import NormalTodo, NeverEndingTodo, PipelineTodo, RepetitiveTodo
from django.contrib import admin

admin.site.register(NormalTodo)
admin.site.register(NeverEndingTodo)
admin.site.register(PipelineTodo)
admin.site.register(RepetitiveTodo)
