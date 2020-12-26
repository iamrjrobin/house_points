from django.apps import AppConfig


class BasicUserConfig(AppConfig):
    name = 'basic_user'

    def ready (self):
        import basic_user.signals