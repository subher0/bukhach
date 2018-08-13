from django.apps import AppConfig

class BukhachConfig(AppConfig):
    name = 'bukhach'

    def ready(self):
        import bukhach.signals.signals