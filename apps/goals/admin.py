from django.contrib import admin
from .models import ProgressMonitor
from .models import Strategy
from .models import Link
from .models import Goal

admin.site.register(ProgressMonitor)
admin.site.register(Strategy)
admin.site.register(Link)
admin.site.register(Goal)
