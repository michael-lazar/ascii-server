from django.apps import AppConfig


class MozzAppConfig(AppConfig):
    name = "ascii.mozz"

    def ready(self):
        import ascii.mozz.signals  # noqa: E402, F401
