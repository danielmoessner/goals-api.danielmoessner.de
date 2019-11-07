from django.apps import AppConfig


class GoalsConfig(AppConfig):
    name = 'mastergoal.goals'

    def ready(self):
        import mastergoal.goals.signals
