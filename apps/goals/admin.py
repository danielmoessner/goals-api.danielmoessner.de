from django.contrib import admin

from apps.goals.models import Goal, Link, ProgressMonitor, Strategy

admin.site.register(Goal)
admin.site.register(Strategy)
admin.site.register(ProgressMonitor)
admin.site.register(Link)
