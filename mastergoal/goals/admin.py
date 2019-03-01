from django.contrib import admin

from .models import ProgressMonitor
from .models import NeverEndingToDo
from .models import RepetitiveToDo
from .models import MultipleToDo
from .models import Strategy
from .models import Link
from .models import ToDo
from .models import Goal

admin.site.register(ProgressMonitor)
admin.site.register(NeverEndingToDo)
admin.site.register(RepetitiveToDo)
admin.site.register(MultipleToDo)
admin.site.register(Strategy)
admin.site.register(ToDo)
admin.site.register(Link)
admin.site.register(Goal)
