from django.db.models import signals
from django.shortcuts import reverse
from django.utils import timezone

from .models import NeverEndingToDo
from .models import RepetitiveToDo
from .models import ToDo
from .models import Goal


# signals
def post_save_target(sender, instance, **kwargs):
    if sender is ToDo:
        if instance.pipeline_to_dos.exists() and instance.is_done:
            instance.pipeline_to_dos.update(activate=timezone.now())
    if sender is RepetitiveToDo:
        if not instance.trash:
            if not instance.get_next():
                instance.generate_next()
    elif sender is NeverEndingToDo:
        if (instance.is_done or instance.has_failed) and not instance.next.all().exists():
            instance.generate_next()
    elif sender is Goal:
        if instance.is_archived:
            instance.get_all_sub_goals().update(is_archived=True)
            instance.get_all_sub_monitors().update(is_archived=True)
            instance.get_all_sub_strategies().update(is_archived=True)
            instance.get_all_sub_todos().update(is_archived=True)
            instance.get_all_sub_links().update(is_archived=True)


signals.post_save.connect(post_save_target, sender=Goal)
signals.post_save.connect(post_save_target, sender=ToDo)
signals.post_save.connect(post_save_target, sender=RepetitiveToDo)
signals.post_save.connect(post_save_target, sender=NeverEndingToDo)
