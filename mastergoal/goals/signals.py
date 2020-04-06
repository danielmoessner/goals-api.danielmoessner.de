from django.db.models import signals
from django.utils import timezone

from .models import NeverEndingToDo
from .models import RepetitiveToDo
from .models import ToDo
from .models import Goal
from .models import Link


# general stuff
def post_save_target(sender, instance, **kwargs):
    if sender is ToDo:
        if instance.pipeline_to_dos.exists() and instance.is_done:
            instance.pipeline_to_dos.update(activate=timezone.now())
    if sender is RepetitiveToDo:
        if instance.repetitions > 0 and instance.get_next() is None:
            instance.generate_next()
    elif sender is NeverEndingToDo:
        if (instance.is_done or instance.has_failed) and not instance.next.all().exists():
            instance.generate_next()


signals.post_save.connect(post_save_target, sender=NeverEndingToDo)
signals.post_save.connect(post_save_target, sender=RepetitiveToDo)
signals.post_save.connect(post_save_target, sender=ToDo)
