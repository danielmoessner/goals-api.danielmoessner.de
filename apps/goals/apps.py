from django.apps import AppConfig


class GoalsConfig(AppConfig):
    name = 'apps.goals'

    def ready(self):
        import apps.goals.signals
