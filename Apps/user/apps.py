from django.apps import AppConfig

class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Apps.user'

    def ready(self):
        import Apps.user.signals
